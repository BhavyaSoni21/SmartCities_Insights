from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from .models import Complaint, UserProfile            
from django.contrib.auth import get_user_model
from .forms import UserForm, ProfileForm
from django.db.models import Count
from django.db.models import Avg, F, ExpressionWrapper, DurationField

def _attach_profile_attrs(request: HttpRequest) -> None:
    user = getattr(request, "user", None)
    if not user or not getattr(user, "is_authenticated", False):
        return

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "name": user.get_full_name() or user.get_username(),
            "role": "Citizen",
            "locality": "",
            "ward_number": "",
        },
    )

    user.name = profile.name or user.get_full_name() or user.get_username()
    user.role = profile.role
    user.locality = profile.locality
    user.ward_number = profile.ward_number
    user.mobile = profile.mobile
    user.age = profile.age

def index(request: HttpRequest) -> HttpResponse:
    citizen_profiles = UserProfile.objects.filter(role='Citizen')

    citizen_complaints = Complaint.objects.filter(
        user__profile__role='Citizen'
    )

    resolved_count = citizen_complaints.filter(status='resolved').count()

    active_citizens = (
        citizen_complaints
        .values('user')
        .distinct()
        .count()
    )

    localities_covered = (
        citizen_profiles
        .exclude(locality='')
        .values('locality')
        .distinct()
        .count()
    )

    context = {
        'resolved_count': resolved_count,
        'active_citizens': active_citizens,
        'localities_covered': localities_covered,
    }

    return render(request, 'index.html', context)

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)

    if request.user.role == 'Admin':
        complaints_qs = Complaint.objects.select_related(
            'user', 'user__profile'
        ).all()

        top_complaints = complaints_qs.filter(
            status='pending'
        ).order_by('-created_at')[:5]
    else:
        complaints_qs = Complaint.objects.filter(user=request.user)
        top_complaints = []

    complaints_qs = complaints_qs.order_by('-created_at')
    
    total_complaints = complaints_qs.count()
    resolved_count = complaints_qs.filter(status='resolved').count()
    pending_count = complaints_qs.filter(status='pending').count()
    
    pending_complaints_list = complaints_qs.filter(status='pending')
    pending_sla_breached = sum(1 for c in pending_complaints_list if c.sla_status == 'breached')
    pending_in_sla = sum(1 for c in pending_complaints_list if c.sla_status == 'active')
    
    sla_breached_count = sum(
        1 for c in complaints_qs if c.sla_status == 'breached'
    )

    resolved_items = complaints_qs.filter(
        status='resolved',
        resolved_at__isnull=False
    )

    total_hours = 0
    resolved_items_count = 0

    for c in resolved_items:
        if c.resolution_time_hours is not None:
            total_hours += c.resolution_time_hours
            resolved_items_count += 1

    avg_resolution_time = (
        round(total_hours / resolved_items_count, 2)
        if resolved_items_count > 0
        else None
    )

    complaints_json = [
        {
            'id': c.id,
            'issue_type': c.issue_type.title(),
            'description': c.description,
            'latitude': c.latitude or 19.0760,
            'longitude': c.longitude or 72.8777,
            'status': c.status,
            'sla_status': c.sla_status,
        }
        for c in complaints_qs
    ]

    recent_activities = [
        {
            'id': c.id,
            'type': (
                'critical' if c.sla_status == 'breached'
                else 'resolved' if c.status == 'resolved'
                else 'new'
            ),
            'description': f"{c.issue_type.title()} near {c.landmark or 'unknown location'}",
            'timestamp': c.resolved_at if c.status == 'resolved' else c.created_at
        }
        for c in complaints_qs[:5]
    ]

    return render(
        request,
        'dashboard.html',
        {
            'total_complaints': total_complaints,
            'resolved_complaints': resolved_count,
            'pending_complaints': pending_count,
            'pending_sla_breached': pending_sla_breached,
            'pending_in_sla': pending_in_sla,
            'sla_breached_count': sla_breached_count,
            'avg_resolution_time': avg_resolution_time,
            'active_reporters': complaints_qs.values('user').distinct().count(),
            'recent_activities': recent_activities,
            'complaints_list': complaints_qs,
            'complaints': complaints_qs,
            'top_complaints': top_complaints,
            'ward_center_lat': 19.0760,
            'ward_center_lng': 72.8777,
            'complaints_json': json.dumps(
                complaints_json, cls=DjangoJSONEncoder
            ),
        },
    )


@login_required
def complaints(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)

    complaints_qs = Complaint.objects.select_related(
        'user', 'user__profile'
    ).all()

    complaints_qs = complaints_qs.order_by('-created_at')

    paginator = Paginator(complaints_qs, 6)
    page_number = request.GET.get('page')
    complaints_page = paginator.get_page(page_number)

    return render(
        request,
        'complaints.html',
        {
            'complaints': complaints_page
        }
    )

@login_required
def complaint_detail(request: HttpRequest, pk: int) -> HttpResponse:
    _attach_profile_attrs(request)
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaint-detail.html', {'complaint': complaint})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    
    user_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    total_complaints = user_complaints.count()
    resolved_complaints = user_complaints.filter(status='resolved').count()
    pending_complaints = user_complaints.filter(status='pending').count()
    
    context = {
        'user_complaints': user_complaints,
        'user_total_complaints': total_complaints,
        'user_resolved_complaints': resolved_complaints,
        'user_pending_complaints': pending_complaints,
    }
    
    return render(request, 'profile.html', context)


@login_required
def register_complaint(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type', 'other')
        description = request.POST.get('description', '')
        landmark = request.POST.get('landmark', '')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        before_image = request.FILES.get('before_image')

        title = f"{issue_type.title()} Issue"
        if landmark:
            title += f" near {landmark}"
        
        Complaint.objects.create(
            user=request.user,
            title=title[:200], 
            description=description,
            issue_type=issue_type,
            landmark=landmark,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            before_image=before_image,
            status='pending'
        )
        
        messages.success(request, 'Complaint submitted successfully.')
        return redirect('complaints')
    return render(request, 'register-complaint.html', {})


@login_required
def admin_dashboard(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    
    if request.user.role != 'Admin':
         pass

    complaints_qs = Complaint.objects.select_related('user').all()
    
    total_complaints = complaints_qs.count()
    resolved_complaints_qs = complaints_qs.filter(status='resolved')
    resolved_complaints = resolved_complaints_qs.count()
    
    pending_complaints_qs = complaints_qs.filter(status='pending')
    pending_complaints = pending_complaints_qs.count()
    
    monthly_complaints = complaints_qs.filter(created_at__month=timezone.now().month).count()
    
    resolution_rate = 0
    if total_complaints > 0:
        resolution_rate = int((resolved_complaints / total_complaints) * 100)

    all_complaints_list = []
    sla_breached_complaints = []
    
    for c in complaints_qs:
        item = c
                
        if c.sla_status == 'breached':
            sla_breached_complaints.append(c)
        
        marker_color = 'orange'
        if c.status == 'resolved':
            marker_color = 'green'
        elif c.sla_status == 'breached':
            marker_color = 'red'

        all_complaints_list.append({
            'id': c.id,
            'issue_type': c.issue_type, 
            'description': c.description,
            'latitude': c.latitude or 19.0760,
            'longitude': c.longitude or 72.8777,
            'status': c.status,
            'sla_status': c.sla_status,
        })
        
    sla_breached_count = sum(
        1 for c in complaints_qs if c.sla_status == 'breached'
    )

    context = {
        'sla_breached_count': sla_breached_count,
        'total_complaints': total_complaints,
        'monthly_complaints': monthly_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'resolution_rate': resolution_rate,
        'sla_breached_complaints': sla_breached_complaints,
        'pending_complaints_list': pending_complaints_qs, 
        'ward_center_lat': 19.0760,
        'ward_center_lng': 72.8777,
        'complaints_json': json.dumps(all_complaints_list, cls=DjangoJSONEncoder),
    }
    
    return render(request, 'admin-dashboard.html', context)


@login_required
def resolve_complaint(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    if request.method != 'POST':
        return redirect('admin_dashboard')
    
    complaint_id = request.POST.get('complaint_id')
    after_image = request.FILES.get('after_image')
    notes = request.POST.get('resolution_notes')
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    complaint.status = 'resolved'
    if after_image:
        complaint.after_image = after_image
    complaint.save()

    messages.success(request, 'Complaint marked as resolved.')
    return redirect('admin_dashboard')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''

        if email == 'demo@city.com' and password == 'demo12345':
            User = get_user_model()
            try:
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={'email': email, 'is_active': True}
                )
                if created:
                    user.set_password(password)
                    user.save()
                    # Create profile
                    UserProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'name': 'Demo User',
                            'role': 'Admin', 
                            'locality': 'Ward 1 - Central District',
                            'ward_number': '1',
                            'mobile': '9999999999',
                            'age': 25,
                        }
                    )
                else: 
                    if hasattr(user, 'profile'):
                        if user.profile.role != 'Admin':
                            user.profile.role = 'Admin'
                            user.profile.save()

                auth_login(request, user)
                _attach_profile_attrs(request)
                messages.success(request, 'Logged in successfully.')
                return redirect('admin_dashboard') 
            except Exception as e:
                messages.error(request, f'Database error. Please register a new account or check database permissions.')
                return render(request, 'login.html', {})

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html', {})

        auth_login(request, user)
        _attach_profile_attrs(request)
        messages.success(request, 'Logged in successfully.')
        
        if getattr(request.user, 'role', 'Citizen') == 'Admin':
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'login.html', {})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        User = get_user_model()
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        name = (request.POST.get('name') or '').strip()
        mobile = (request.POST.get('mobile') or '').strip()
        age_raw = (request.POST.get('age') or '').strip()
        locality = (request.POST.get('locality') or '').strip()

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'register.html', {})

        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists. Please log in.')
            return redirect('login')

        user = User.objects.create_user(username=email, email=email, password=password)
        profile = UserProfile.objects.create(
            user=user,
            name=name or email,
            role='Citizen',
            locality=locality,
            ward_number='',
            mobile=mobile,
            age=int(age_raw) if age_raw.isdigit() else None,
        )
        profile.save()

        messages.success(request, 'Account created. Please log in.')
        return redirect('login')
    return render(request, 'register.html', {})


def logout_view(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return redirect(reverse('index'))

@login_required
def profile_settings(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_settings')

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'settings.html', {   
        'user_form': user_form,
        'profile_form': profile_form
    })

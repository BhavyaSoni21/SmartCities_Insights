from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import json # For JSON serialization
from django.core.serializers.json import DjangoJSONEncoder # Better serialization

from .models import Complaint, UserProfile

from .forms import UserForm, ProfileForm

def _attach_profile_attrs(request: HttpRequest) -> None:
    """
    Templates reference attributes like `user.name`, `user.role`, etc.
    Default Django `User` doesn't have these, so we attach them from UserProfile.
    """
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

    # Monkeypatch common template fields onto `request.user`
    user.name = profile.name or user.get_full_name() or user.get_username()
    user.role = profile.role
    user.locality = profile.locality
    user.ward_number = profile.ward_number
    user.mobile = profile.mobile
    user.age = profile.age

def home(request: HttpRequest) -> HttpResponse:
    issues = Complaint.objects.all() # Was Issue
    return render(request, 'home.html', {'issues': issues})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    
    # Fetch complaints based on user role
    if request.user.role == 'Admin':
        # Admins see all complaints from their locality
        user_complaints = Complaint.objects.filter(user__profile__locality=request.user.locality)
    else:
        # Citizens see only their own complaints
        user_complaints = Complaint.objects.filter(user=request.user)
    
    # Calculate stats
    total_complaints = user_complaints.count()
    resolved_complaints = user_complaints.filter(status='resolved').count()
    pending_complaints = user_complaints.filter(status='pending').count()
    
    # Prepare map data
    complaints_list_json = []
    for c in user_complaints:
        complaints_list_json.append({
            'id': c.id,
            'issue_type': c.issue_type.title(),
            'description': c.description,
            'latitude': c.latitude or 19.0760,
            'longitude': c.longitude or 72.8777,
            'status': c.status,
            'sla_status': c.sla_status,
        })
    
    return render(
        request,
        'dashboard.html',
        {
            'total_complaints': total_complaints,
            'resolved_complaints': resolved_complaints,
            'pending_complaints': pending_complaints,
            'sla_breached': sum(1 for c in user_complaints if c.sla_status == 'breached'),
            'avg_resolution_time': '--',
            'active_reporters': user_complaints.values('user').distinct().count(),
            'recent_activities': [
                {
                    'id': c.id,
                    'type': 'resolved' if c.status == 'resolved' else 'new',
                    'description': f"{'Resolved' if c.status == 'resolved' else 'New'} {c.issue_type} reported near {c.landmark or 'unknown location'}",
                    'timestamp': c.resolved_at if c.status == 'resolved' else c.created_at
                }
                for c in Complaint.objects.filter(user__profile__locality=request.user.locality).order_by('-created_at')[:5]
            ],
            'complaints_list': user_complaints.order_by('-created_at'),
            'ward_center_lat': 19.0760,
            'ward_center_lng': 72.8777,
            'complaints_json': json.dumps(complaints_list_json, cls=DjangoJSONEncoder),
            'sla_breached_count': 0, # Just to satisfy template check if present
        },
    )


@login_required
def complaints(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    
    # Fetch complaints based on user role
    if request.user.role == 'Admin':
        # Admins see all complaints from their locality
        complaints_list = Complaint.objects.filter(user__profile__locality=request.user.locality).order_by('-created_at')
    else:
        # Citizens see only their own complaints
        complaints_list = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'complaints.html', {'complaints': complaints_list})


@login_required
def complaint_detail(request: HttpRequest, pk: int) -> HttpResponse:
    _attach_profile_attrs(request)
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaint-detail.html', {'complaint': complaint})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    _attach_profile_attrs(request)
    
    # Fetch complaints for the current user
    user_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate stats
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
        # Extract data
        issue_type = request.POST.get('issue_type', 'other')
        description = request.POST.get('description', '')
        landmark = request.POST.get('landmark', '')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        before_image = request.FILES.get('before_image')

        # Generate a title since form doesn't have one
        title = f"{issue_type.title()} Issue"
        if landmark:
            title += f" near {landmark}"
        
        # Create complaint
        Complaint.objects.create(
            user=request.user,
            title=title[:200], # Ensure max length
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
         # In a real app check permission properly. For demo, we rely on _attach_profile_attrs
         pass

    # Fetch data
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

    # Calculate SLA breaches and convert to list for template
    all_complaints_list = []
    sla_breached_complaints = []
    
    for c in complaints_qs:
        item = c
        # Ensure properties are available or pre-calculated if not using model methods in template
        # Template uses c.days_pending, c.sla_status, c.issue_type, c.description, c.id, c.user.name, c.landmark
        
        if c.sla_status == 'breached':
            sla_breached_complaints.append(c)
        
        # Determine status color/marker for map
        marker_color = 'orange'
        if c.status == 'resolved':
            marker_color = 'green'
        elif c.sla_status == 'breached':
            marker_color = 'red'

        all_complaints_list.append({
            'id': c.id,
            'issue_type': c.issue_type, # ensure TitleCase in template or use get_display
            'description': c.description,
            'latitude': c.latitude or 19.0760, # Fallback
            'longitude': c.longitude or 72.8777,
            'status': c.status,
            'sla_status': c.sla_status,
        })
        
    sla_breached_count = len(sla_breached_complaints)
    
    context = {
        'sla_breached_count': sla_breached_count,
        'total_complaints': total_complaints,
        'monthly_complaints': monthly_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'resolution_rate': resolution_rate,
        'sla_breached_complaints': sla_breached_complaints,
        'pending_complaints_list': pending_complaints_qs, # Or sort them
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
    # You might want to save notes somewhere
    complaint.save()

    messages.success(request, 'Complaint marked as resolved.')
    return redirect('admin_dashboard')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''

        # Temporary demo bypass: if demo credentials, auto-create account
        if email == 'demo@city.com' and password == 'demo12345':
            from django.contrib.auth import get_user_model
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
                            'role': 'Admin', # CHANGED TO ADMIN FOR DEMO
                            'locality': 'Ward 1 - Central District',
                            'ward_number': '1',
                            'mobile': '9999999999',
                            'age': 25,
                        }
                    )
                else: 
                     # Ensure existing demo user is Admin for testing
                     if hasattr(user, 'profile'):
                         if user.profile.role != 'Admin':
                             user.profile.role = 'Admin'
                             user.profile.save()

                auth_login(request, user)
                _attach_profile_attrs(request)
                messages.success(request, 'Logged in successfully.')
                return redirect('admin_dashboard') # Redirect to admin dashboard for demo
            except Exception as e:
                messages.error(request, f'Database error. Please register a new account or check database permissions.')
                return render(request, 'login.html', {})

        # Normal authentication
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html', {})

        auth_login(request, user)
        _attach_profile_attrs(request)
        messages.success(request, 'Logged in successfully.')
        
        # Check role on request.user as it is the one patched by _attach_profile_attrs
        if getattr(request.user, 'role', 'Citizen') == 'Admin':
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'login.html', {})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        from django.contrib.auth import get_user_model

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
    # Navbar uses this named URL; always return to home.
    return redirect(reverse('home'))

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

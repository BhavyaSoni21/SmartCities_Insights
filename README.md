# SmartCity Insight  
**Urban Issue Management Platform | SDG 11 Aligned**

SmartCity Insight is a responsive, role-based web application designed to streamline urban issue reporting and resolution. Built with a strong civic-first design philosophy, the platform empowers citizens and administrators to collaboratively improve city infrastructure while aligning with **UN SDG 11: Sustainable Cities and Communities**.

---

## Purpose

Cities don’t fail because problems don’t exist.  
They fail because problems aren’t tracked, visualized, or resolved on time.

SmartCity Insight fixes that.

---

## Key Highlights

- Role-based access (Citizen / Admin)
- Locality-wise complaint tracking
- SLA-based accountability system
- Interactive maps and data visualization
- Mobile-first, government-grade UI
- Built for transparency, not aesthetics alone

---

## Design System

**Visual Tone**: Civic, professional, accountable  

**Typography**
- Display: **Bitter** (serif)
- Body: **Work Sans** (sans-serif)

**Color Palette**
```css
:root {
  --primary-color: #1e5a3f;   /* Forest Green */
  --secondary-color: #d97706; /* Amber */
  --success-color: #2a9d4e;
  --warning-color: #f59e0b;
  --danger-color: #dc2626;
}
````

---

## Project Structure
```
SmartCities_Insights/
│
├── SmartCities/          # Project
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                 # App
│   ├── migrations/
│   ├── templates/
│   │   ├── navbar.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── complaints.html
│   │   ├── complaint-detail.html
│   │   ├── register-complaint.html
│   │   ├── profile.html
|   |   ├── admin-dashboard.html
│   │   └── styles.css
│   │
|   ├── admin.py
|   ├── app.py   
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── media/
│   └── complaints/
│       ├── before/
│       └── after/
|
├── check_db.py
├── db.sqlite3
├── manage.py
└── README.md
```
---

## Pages & Access Levels (Actual File Mapping)

### Public Pages (No Login Required)

* **`index.html`**
  Landing page introducing SmartCity Insight.
  No complaint data, no privileged actions.

* **`login.html`**
  User authentication page for citizens and admins.

* **`register.html`**
  Citizen registration page.

---

### Authenticated Pages (Login Required)

* **`dashboard.html`**
  Locality-level dashboard showing complaint statistics, status distribution, and recent activity.

* **`register-complaint.html`**
  Complaint submission form with:

  * Issue type selection
  * Interactive map for location
  * Image upload (before image)

* **`complaints.html`**
  Complaint listing page with filtering by status, issue type, and SLA condition.

* **`complaint-detail.html`**
  Detailed view of a single complaint including timeline, images, and status history.

* **`profile.html`**
  User profile page displaying personal complaint history and account details.

* **`settings.html`**
  User account settings and configuration page.

---

### Admin-Only Pages

* **`admin-dashboard.html`**
  Administrative control panel featuring:

  * Pending and SLA-breached complaints
  * Resolution workflow with image upload
  * Ward-level monitoring and management tools

---

### Shared Components

* **`navbar.html`**
  Reusable navigation component included across all pages.
  Renders different options based on authentication state and user role.

---

### Note on Styles

* **`styles.css`**
  Currently located inside the `templates` directory.
  This file should be moved to a proper static directory for correct Django usage.
  
---

## Access Control Logic

```django
{% if user.is_authenticated %}
  <!-- Protected Content -->
{% endif %}

{% if user.is_authenticated and user.role == 'Admin' %}
  <!-- Admin Tools -->
{% endif %}
```

---

## SLA System

| Issue Type  | SLA Time |
| ----------- | -------- |
| Garbage     | 24 hrs   |
| Pothole     | 72 hrs   |
| Streetlight | 48 hrs   |
| Other       | 72 hrs   |

**Status Indicators**

* 🟢 Within SLA
* 🔴 SLA Breached

Backend calculates:

* `hrs_pending`
* `sla_status`
* `avg_resolution_time`

---

## Tech Stack

### Frontend

* HTML5, CSS3
* Vanilla JavaScript
* Chart.js (Data Visualization)
* Leaflet.js (Maps)

### Backend (Expected)

* Django
* SQLite / PostgreSQL
* Django Auth System

---

## Django URL Configuration

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complaints/', views.complaints, name='complaints'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('profile/', views.profile, name='profile'),
    path('register-complaint/', views.register_complaint, name='register_complaint'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('resolve-complaint/', views.resolve_complaint, name='resolve_complaint'),
    path('settings/', views.profile_settings, name='profile_settings'),
]
```
---

## Required Context Variables (Template-Aligned)

These context variables are expected to be provided by Django views to properly render each template.

---

### `dashboard.html`

```python
{
  'total_complaints': int,
  'resolved_complaints': int,
  'pending_complaints': int,
  'sla_breached': int,
  'recent_activities': QuerySet,   # Recent complaints or status updates
  'user': request.user
}
```

Used for:

* KPI cards
* Status distribution charts
* Recent activity feed

---

### `complaints.html`

```python
{
  'complaints': QuerySet,           # Paginated list of complaints
  'status_filter': str | None,
  'issue_filter': str | None,
  'sla_filter': str | None
}
```

Each complaint object should expose:

* `id`
* `issue_type`
* `description`
* `status`
* `created_at`
* `days_pending`
* `sla_status`
* `before_image`
* `after_image`

---

### `complaint-detail.html`

```python
{
  'complaint': Complaint,           # Single complaint instance
  'timeline': list,                 # Status change history (optional)
  'is_admin': bool
}
```

Used for:

* Full complaint lifecycle view
* Image comparison (before / after)
* Resolution notes

---

### `profile.html`

```python
{
  'user': request.user,
  'user_complaints': QuerySet,
  'total_reported': int,
  'resolved_count': int,
  'pending_count': int
}
```

Used for:

* Personal complaint statistics
* User-specific history

---

### `settings.html`

```python
{
  'user': request.user,
  'profile_form': DjangoForm
}
```

Used for:

* Account updates
* Profile configuration

---

### `admin-dashboard.html` (Admin Only)

```python
{
  'total_complaints': int,
  'pending_complaints': int,
  'resolved_complaints': int,
  'sla_breached_count': int,
  'pending_complaints_list': QuerySet,
  'sla_breached_complaints': QuerySet,
  'complaints_json': str,            # Serialized for map markers
  'ward_center_lat': float,
  'ward_center_lng': float
}
```

Used for:

* Administrative monitoring
* SLA enforcement
* Complaint resolution workflow
* Map visualization

---

### Global (Used Across Templates)

```python
{
  'user': request.user
}
```

Available implicitly via Django’s request context.

---

## Responsive Breakpoints

* Desktop: ≥1200px
* Tablet: 768px – 1199px
* Mobile: <768px

---

## Deployment Checklist

* Django auth configured
* MEDIA_ROOT / MEDIA_URL set
* CSRF protection enabled
* Image uploads tested
* SLA logic implemented
* Admin access restricted
* Responsive testing done

---

## Project Significance

SmartCity Insight models a real-world urban grievance system rather than a generic CRUD application.

The project demonstrates:
- Domain-driven problem modeling for civic infrastructure
- Role-based access control (Citizen vs Admin)
- SLA-backed accountability and status tracking
- Data visualization for operational transparency
- A scalable UI structure aligned with real municipal workflows

This makes the project suitable for:
- Academic evaluation and final-year submissions
- Resume and portfolio demonstrations
- Smart city and civic-tech concept demos


---

## SDG Alignment

**UN Sustainable Development Goal 11 – Sustainable Cities and Communities**

SmartCity Insight aligns with SDG 11 by providing a structured digital system for reporting, tracking, and resolving urban infrastructure issues at the locality level.

The platform supports this goal through:
- Transparent complaint reporting and tracking
- SLA-based accountability for civic issue resolution
- Data-driven visibility into urban service performance
- Role-based participation by citizens and administrators

Rather than treating sustainability as a concept, the system operationalizes it through measurable workflows and outcomes.

### All rights reserved © 2026 SmartCity Insight/BhavyaSoni21

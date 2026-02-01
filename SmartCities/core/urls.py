from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
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

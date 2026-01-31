from django.contrib import admin
from .models import Complaint, UserProfile

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue_type', 'status', 'sla_status', 'created_at')
    list_filter = ('status', 'issue_type')
    search_fields = ('title', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'locality')


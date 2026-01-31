from django.db import models
from django.conf import settings

from django.utils import timezone

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]
    ISSUE_TYPE_CHOICES = [
        ('garbage', 'Garbage'),
        ('pothole', 'Pothole'),
        ('streetlight', 'Streetlight'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES, default='other')
    
    landmark = models.CharField(max_length=200, blank=True, help_text="Nearby landmark or location name")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    before_image = models.ImageField(upload_to='complaints/before/', blank=True, null=True)
    after_image = models.ImageField(upload_to='complaints/after/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def days_pending(self):
        if self.status == 'resolved':
            return 0
        return (timezone.now() - self.created_at).days

    @property
    def sla_status(self):
        # Example SLA: 3 days
        if self.status != 'resolved' and self.days_pending > 3:
            return 'breached'
        return 'active'

    @property
    def days_overdue(self):
        if self.sla_status == 'breached':
            return self.days_pending - 3
        return 0

    def __str__(self):
        return f"{self.issue_type} - {self.title}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Citizen', 'Citizen'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200, blank=True, default='')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Citizen')
    locality = models.CharField(max_length=200, blank=True, default='')
    ward_number = models.CharField(max_length=50, blank=True, default='')
    mobile = models.CharField(max_length=20, blank=True, default='')
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name or self.user.get_username()

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

    SLA_TIERS = {
        'garbage': 24,
        'streetlight': 48,
        'pothole': 72,
        'other': 72,
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    issue_type = models.CharField(
        max_length=50,
        choices=ISSUE_TYPE_CHOICES,
        default='other'
    )

    landmark = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    before_image = models.ImageField(
        upload_to='complaints/before/',
        blank=True,
        null=True
    )
    after_image = models.ImageField(
        upload_to='complaints/after/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def sla_hours(self) -> int:
        """Return SLA hours based on issue type"""
        return self.SLA_TIERS.get(self.issue_type, 72)

    @property
    def hours_pending(self) -> int:
        """Total hours since complaint was created"""
        end_time = self.resolved_at or timezone.now()
        delta = end_time - self.created_at
        return int(delta.total_seconds() // 3600)

    @property
    def sla_status(self) -> str:
        if self.status == 'resolved':
            return 'breached' if self.hours_pending > self.sla_hours else 'resolved'

        return 'breached' if self.hours_pending > self.sla_hours else 'active'


    @property
    def sla_hours_remaining(self):
        if self.status != 'pending':
            return None
        return max(0, self.sla_hours - self.hours_pending)


    @property
    def sla_hours_overdue(self):
        if self.hours_pending > self.sla_hours:
            return self.hours_pending - self.sla_hours
        return 0


    def __str__(self):
        return f"{self.issue_type.upper()} | {self.title}"

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
        if self.status != 'resolved' and self.hours_pending > self.SLA_TIERS.get(self.issue_type, 3):
            return 'breached'
        return 'active'

    @property
    def hours_overdue(self):
        if self.sla_status == 'breached':
            return self.hours_pending - self.SLA_TIERS.get(self.issue_type, 3)
        return 0

    def __str__(self):
        return f"{self.issue_type} - {self.title}"

    @property
    def resolution_time_hours(self):
        if self.status != 'resolved' or not self.resolved_at:
            return None

        delta = self.resolved_at - self.created_at
        return round(delta.total_seconds() / 3600, 2)


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


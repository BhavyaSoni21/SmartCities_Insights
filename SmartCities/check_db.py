import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCities.settings')
django.setup()

from core.models import Complaint, UserProfile
from django.contrib.auth.models import User

print(f"Users count: {User.objects.count()}")
print(f"Profiles count: {UserProfile.objects.count()}")
print(f"Complaints count: {Complaint.objects.count()}")

complaints = Complaint.objects.all()[:5]
for c in complaints:
    print(f"Complaint {c.id}: Status={c.status}, User={c.user}, Created={c.created_at}")
    try:
        print(f"  - SLA Status: {c.sla_status}")
    except Exception as e:
        print(f"  - Error getting SLA Status: {e}")
    try:
        print(f"  - Days Pending: {c.days_pending}")
    except Exception as e:
        print(f"  - Error getting Days Pending: {e}")

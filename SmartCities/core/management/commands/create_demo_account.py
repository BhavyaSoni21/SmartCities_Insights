from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import UserProfile


class Command(BaseCommand):
    help = "Create demo login account(s) for local development."

    def handle(self, *args, **options):
        User = get_user_model()

        email = "demo@city.com"
        password = "demo12345"

        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email},
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: {email}"))
        else:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Updated password for: {email}"))

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "name": "Admin",
                "role": "Admin",
                "locality": "Mumbai",
                "ward_number": "Entire Mumbai",
                "mobile": "9999999999",
                "age": 25,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo account is ready:"))
        self.stdout.write(f"  email/username: {email}")
        self.stdout.write(f"  password: {password}")

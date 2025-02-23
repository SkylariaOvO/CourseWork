from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import UserProfile

class Command(BaseCommand):
    help = "Ensure every user has a UserProfile"

    def handle(self, *args, **kwargs):
        created_profiles = 0
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                created_profiles += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created_profiles} missing profiles!"))

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up demo users with passwords from environment variables'

    def handle(self, *args, **options):
        # Get demo password from environment variable
        demo_password = os.getenv('DEMO_USER_PASSWORD')
        if not demo_password:
            self.stdout.write(
                self.style.ERROR('DEMO_USER_PASSWORD environment variable not set')
            )
            return

        # Create demo student
        student_user, created = User.objects.get_or_create(
            username='john.doe',
            defaults={
                'email': 'john.doe@university.edu',
                'role': User.STUDENT,
                'is_active': True
            }
        )
        student_user.set_password(demo_password)
        student_user.save()

        # Create demo faculty
        faculty_user, created = User.objects.get_or_create(
            username='prof.johnson',
            defaults={
                'email': 'prof.johnson@university.edu',
                'role': User.FACULTY,
                'is_active': True
            }
        )
        faculty_user.set_password(demo_password)
        faculty_user.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully set up demo users with passwords from environment variables')
        ) 
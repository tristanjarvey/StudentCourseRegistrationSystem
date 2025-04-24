from django.core.management.base import BaseCommand
from admin_dashboard.models import Building, Classroom


class Command(BaseCommand):
    help = 'Seeds the database with sample buildings and classrooms'

    def handle(self, *args, **kwargs):
        # Clear existing data (optional)
        Classroom.objects.all().delete()
        Building.objects.all().delete()

        buildings = [
            Building.objects.create(name="Engineering and Math Science Building"),
            Building.objects.create(name="Chemistry Building"),
            Building.objects.create(name="Physics Building"),
            Building.objects.create(name="Mitchell Hall"),
        ]

        classrooms = [
            Classroom(building=buildings[0], room_number="E190", capacity=100),
            Classroom(building=buildings[1], room_number="233", capacity=15),
            Classroom(building=buildings[2], room_number="145", capacity=20),
            Classroom(building=buildings[3], room_number="154", capacity=50),
        ]

        Classroom.objects.bulk_create(classrooms)

        self.stdout.write(self.style.SUCCESS('Successfully seeded buildings and classrooms!'))

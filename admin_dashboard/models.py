from django.db import models


class Building(models.Model):
    building_id = models.CharField(max_length=10, unique=True, null=True, blank=True, help_text="Building ID (e.g., 'EMS' for Engineering and Math Science)")
    name = models.CharField(max_length=100, unique=True)

    objects: models.Manager['Building'] = models.Manager()

    def __str__(self):
        return f"{self.building_id} - {self.name}" if self.building_id else self.name


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=15, unique=True, null=True, blank=True, help_text="Classroom ID (e.g., 'EMS-E190')")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classrooms')
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()

    objects: models.Manager['Classroom'] = models.Manager()

    class Meta:
        unique_together = ('building', 'room_number')

    def __str__(self):
        if self.classroom_id:
            return f"{self.classroom_id} - {self.building.name} Room {self.room_number}"
        return f"{self.building.name} - Room {self.room_number}"

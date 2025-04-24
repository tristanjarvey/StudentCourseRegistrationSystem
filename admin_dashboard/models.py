from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects: models.Manager['Building'] = models.Manager()

    def __str__(self):
        return self.name


class Classroom(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='classrooms')
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()

    objects: models.Manager['Classroom'] = models.Manager()

    class Meta:
        unique_together = ('building', 'room_number')

    def __str__(self):
        return f"{self.building.name} - Room {self.room_number}"

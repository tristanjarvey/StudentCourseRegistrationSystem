from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_for')

    def __str__(self):
        return f"{self.name} ({self.department})"

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length=10)  # e.g., 'MWF', 'TR'

    def __str__(self):
        return f"{self.course.name} - {self.semester} ({self.instructor})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} -> {self.section.course.name} ({self.section.semester})"

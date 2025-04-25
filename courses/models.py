from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class Prerequisite(models.Model):
    course = models.ForeignKey(Course, related_name='main_course', on_delete=models.CASCADE)
    prerequisite = models.ForeignKey(Course, related_name='prerequisite_course', on_delete=models.CASCADE)

class Semester(models.Model):
    name = models.CharField(max_length=50)  # e.g. "Fall 2025"
    start_date = models.DateField()
    end_date = models.DateField()

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=10)
    instructor = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    location = models.CharField(max_length=100)    

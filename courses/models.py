from django.db import models
from users.models import Faculty
from admin_dashboard.models import Building, Classroom


class Department(models.Model):
    dept_id = models.CharField(max_length=10, unique=True, null=True, blank=True, help_text="Department ID (e.g., 'CS' for Computer Science)")
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.dept_id} - {self.name}" if self.dept_id else self.name


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def total_students(self):
        """Calculate total number of students enrolled in all sections of this course."""
        from registrations.models import Enrollment
        return Enrollment.objects.filter(section__course=self).count()


class Prerequisite(models.Model):
    course = models.ForeignKey(Course, related_name='main_course', on_delete=models.CASCADE)
    prerequisite = models.ForeignKey(Course, related_name='prerequisite_course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'prerequisite')

    def __str__(self):
        return f"{self.course.code} requires {self.prerequisite.code}"


class Semester(models.Model):
    semester_id = models.CharField(max_length=10, unique=True, null=True, blank=True, help_text="Semester ID (e.g., 'F2025' for Fall 2025)")
    name = models.CharField(max_length=50)  # e.g. "Fall 2025"
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.semester_id} - {self.name}" if self.semester_id else self.name


class Section(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    TIME_SLOTS = [
        ('08:00-09:15', '8:00 AM - 9:15 AM'),
        ('09:30-10:45', '9:30 AM - 10:45 AM'),
        ('11:00-12:15', '11:00 AM - 12:15 PM'),
        ('12:30-13:45', '12:30 PM - 1:45 PM'),
        ('14:00-15:15', '2:00 PM - 3:15 PM'),
        ('15:30-16:45', '3:30 PM - 4:45 PM'),
        ('17:00-18:15', '5:00 PM - 6:15 PM'),
        ('18:30-19:45', '6:30 PM - 7:45 PM'),
    ]

    section_id = models.CharField(max_length=15, unique=True, null=True, blank=True, help_text="Section ID (e.g., 'CS201-F01')")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=10)
    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='teaching_sections')
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK, null=True, blank=True)
    time_slot = models.CharField(max_length=11, choices=TIME_SLOTS, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField(default=30, help_text="Maximum number of students allowed in this section")

    def __str__(self):
        return f"{self.section_id} - {self.course.name}" if self.section_id else f"{self.section_number} - {self.course.name}"

    @property
    def schedule_display(self):
        """Return a formatted string of the section's schedule."""
        return f"{self.get_day_display()} {self.get_time_slot_display()}"

    @property
    def professor_display(self):
        """Return a formatted string of the professor's name."""
        if self.instructor:
            return f"{self.instructor.name} {self.instructor.last_name}"
        return "TBA"

    @property
    def building_display(self):
        """Return a formatted string of the building name."""
        if self.building:
            return self.building.name
        return "TBA"

    @property
    def classroom_display(self):
        """Return a formatted string of the classroom number."""
        if self.classroom:
            return self.classroom.room_number
        return "TBA"

    @property
    def location_display(self):
        """Return a formatted string of the section's location."""
        if self.classroom and self.building:
            return f"{self.building.name} {self.classroom.room_number}"
        return "TBA"    
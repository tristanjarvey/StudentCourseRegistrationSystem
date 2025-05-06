from django.db import models
from users.models import Student


class Enrollment(models.Model):
    enrollment_id = models.CharField(max_length=30, unique=True, null=True, blank=True, help_text="Enrollment ID (e.g., 'S123456-CS201-F202501')")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey('courses.Section', on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'section')

    def __str__(self):
        if self.enrollment_id:
            return f"{self.enrollment_id} - {self.student.student_name} {self.student.student_last_name} -> {self.section.course.name}"
        return f"{self.student.student_name} {self.student.student_last_name} -> {self.section.course.name}"

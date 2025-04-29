from django.db import models
from sample.student import Student


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey('courses.Section', on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'section')

    def __str__(self):
        return f"{self.student.user.username} -> {self.section.course.name} ({self.section.semester})"

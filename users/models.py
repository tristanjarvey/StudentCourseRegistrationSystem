from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.Model):
    role_id = models.CharField(max_length=10, unique=True, null=True, blank=True, help_text="Role ID (e.g., 'STU' for Student)")
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.role_id} - {self.name}" if self.role_id else self.name


class CustomUser(AbstractUser):
    """Custom user model that extends Django's AbstractUser."""
    STUDENT = 'student'
    FACULTY = 'faculty'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (FACULTY, 'Faculty'),
        (ADMIN, 'Admin'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )
    
    # Add related_name to resolve reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def is_student(self):
        return self.role == self.STUDENT

    def is_faculty(self):
        return self.role == self.FACULTY

    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Student model with OneToOne link to CustomUser
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=50)
    student_last_name = models.CharField(max_length=50)
    degree_program = models.CharField(max_length=100)
    enrollment_year = models.IntegerField()

    class Meta:
        unique_together = ('student_name', 'student_last_name', 'student_id')

    def __str__(self):
        return f"{self.student_id} - {self.student_name} {self.student_last_name}"

    @property
    def student_display(self):
        """Return a formatted string of the student's name."""
        return f"{self.student_name} {self.student_last_name}"


# Faculty model with OneToOne link to CustomUser
class Faculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    office = models.CharField(max_length=50)

    class Meta:
        unique_together = ('name', 'last_name', 'employee_id')

    def __str__(self):
        return f"{self.employee_id} - {self.name} {self.last_name}"
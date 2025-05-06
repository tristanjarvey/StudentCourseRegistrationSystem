from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Faculty, Student, UserRole
from django import forms #new add on


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_last_name','student_id', 'degree_program', 'enrollment_year']


class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'last_name','employee_id', 'department', 'title', 'office']

class RegisterUserForm(UserCreationForm):
    role = forms.ModelChoiceField(
        queryset=UserRole.objects.all(),
        required=True,
        empty_label="-- Select Role --",  # Acts like a placeholder in the dropdown
        label="Role"
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "role", "password1", "password2")
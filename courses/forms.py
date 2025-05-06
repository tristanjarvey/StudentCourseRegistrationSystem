from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credits', 'department']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        } 
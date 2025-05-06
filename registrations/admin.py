from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'section', 'date_registered', 'grade')
    list_filter = ('section__semester', 'grade')
    search_fields = ('student__user__username', 'section__course__name')
    date_hierarchy = 'date_registered'
    ordering = ('-date_registered',)

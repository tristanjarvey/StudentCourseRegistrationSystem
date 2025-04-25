from django.contrib import admin
from .models import  Department, Course, Prerequisite, Semester, Section

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Prerequisite)
admin.site.register(Semester)
admin.site.register(Section)

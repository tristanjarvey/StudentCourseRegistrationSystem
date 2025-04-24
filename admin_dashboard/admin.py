from django.contrib import admin
from .models import Building, Classroom


# Register your models here.
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'room_number', 'capacity')
    list_filter = ('building',)
    search_fields = ('room_number',)

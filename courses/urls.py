"""
URL configuration for student_registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Common URLs (accessible by all authenticated users)
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('sections/', views.section_list, name='section_list'),
    path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    
    # Student URLs
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-schedule/', views.my_schedule, name='my_schedule'),
    path('enroll/<int:section_id>/', views.enroll, name='enroll'),
    path('unenroll/<int:section_id>/', views.unenroll, name='unenroll'),
    
    # Faculty/Admin URLs
    path('course/create/', views.course_create, name='course_create'),
    path('course/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('course/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('section/<int:section_id>/manage/', views.section_manage, name='section_manage'),
    path('enrollment/<int:enrollment_id>/update-grade/', views.update_grade, name='update_grade'),
    
    # Section URLs
    path('section/<int:section_id>/edit/', views.section_edit, name='section_edit'),
    path('section/<int:section_id>/delete/', views.section_delete, name='section_delete'),
    path('section/create/', views.section_create, name='section_create'),
]
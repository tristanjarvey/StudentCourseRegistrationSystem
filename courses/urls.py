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
    # Course listings
    path('', views.course_list, name='course_list'),

    # Course detail
    path('<int:course_id>/', views.course_detail, name='course_detail'),

    # Course management (for instructors/admins)
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/delete/', views.delete_course, name='delete_course'),

    # Course sections
    path('<int:course_id>/sections/', views.section_list, name='section_list'),
    path('<int:course_id>/sections/create/', views.create_section, name='create_section'),
    path('sections/<int:section_id>/', views.section_detail, name='section_detail'),
]
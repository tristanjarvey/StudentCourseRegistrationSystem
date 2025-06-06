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

# from django.urls import path, include
# from . import views
# from django.contrib import admin
# from django.contrib.auth import views as auth_views
# from django.urls import include, path

app_name = 'registrations'


urlpatterns = [
    # Admin page
    # path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),
    #
    # # Login page (for unauthenticated users)
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    #
    # # Student registration views
    # path('', views.course_registration, name='course_registration'),  # Home page
    # path('drop/<int:enrollment_id>/', views.drop_course, name='drop_course'),
    # path('schedule/', views.student_schedule, name='student_schedule'),

    # Additional paths can be added here
    # path('another_view/', views.another_view, name='another_view'),
]




    # Student registration views
    # path('', views.registration_dashboard, name='dashboard'),
    # path('register/<int:section_id>/', views.register_for_section, name='register_section'),
    # path('drop/<int:registration_id>/', views.drop_section, name='drop_section'),


    # Registration management (for admins/instructors)
    # path('manage/', views.manage_registrations, name='manage'),
    # path('section/<int:section_id>/registrations/', views.section_registrations, name='section_registrations'),

    # Waitlist management
    #path('waitlist/', views.waitlist_management, name='waitlist'),

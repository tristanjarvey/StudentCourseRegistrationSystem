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
# from django.urls import path
# from . import views
# from .views import BuildingsView

app_name = 'admin_dashboard'

urlpatterns = [
    # Home page
    # path('', views.dashboard_home, name='admin_dashboard_home'),

    # # Manage users
    # path('users/', views.manage_users, name='manage_users'),
    #
    # # Manage courses
    # path('courses/', views.manage_courses, name='manage_courses'),

    # Admin-specific views
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # path('', BuildingsView.as_view()),
]

from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'registrations'

urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    # Login page (for unauthenticated users)
    path('login/', views.LoginView.as_view(), name='login'),

    # Student registration views
    path('', views.course_registration, name='course_registration'),
    path('drop/<int:enrollment_id>/', views.drop_course, name='drop_course'),
    path('schedule/', views.student_schedule, name='student_schedule'),
]

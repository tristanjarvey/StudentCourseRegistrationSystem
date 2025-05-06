from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    
    # Dashboard URLs
    path('dashboard/', views.home, name='home'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/student/', views.StudentProfileView.as_view(), name='student_profile'),
    path('profile/faculty/', views.FacultyProfileView.as_view(), name='faculty_profile'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Faculty Admin URLs
    path('faculty/admin/', views.faculty_admin_dashboard, name='faculty_admin_dashboard'),
    
    # Student URLs
    path('student/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:student_id>/delete/', views.student_delete, name='student_delete'),
    path('student/create/', views.student_create, name='student_create'),
    
    # Faculty URLs
    path('faculty/<int:faculty_id>/edit/', views.faculty_edit, name='faculty_edit'),
    path('faculty/<int:faculty_id>/delete/', views.faculty_delete, name='faculty_delete'),
    path('faculty/create/', views.faculty_create, name='faculty_create'),
]
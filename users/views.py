from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from .forms import RegisterUserForm, StudentProfileForm, FacultyProfileForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from .models import Student, Faculty, CustomUser
from courses.models import Department
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Section
from registrations.models import Enrollment
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

# Access control decorators
def is_faculty(user):
    return user.is_faculty()

def is_admin(user):
    return user.is_admin()

def is_student(user):
    return user.is_student()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # Keep the form field as 'email' for UI consistency
        password = request.POST.get('password')
        
        # Authenticate user using username
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('courses:my_courses')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')

@login_required
def student_dashboard(request):
    """Display student dashboard with enrolled courses and statistics."""
    try:
        student = request.user.student
        # Get enrolled courses
        enrollments = Enrollment.objects.filter(student=student).select_related(
            'section__course',
            'section__instructor'
        )
        
        context = {
            'enrollments': enrollments,
        }
        return render(request, 'dashboard/student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first.')
        return redirect('users:student_profile')

@login_required
def faculty_dashboard(request):
    """Display faculty dashboard with teaching schedule and statistics."""
    try:
        faculty = request.user.faculty
        teaching_sections = Section.objects.filter(instructor=faculty)
        
        # Calculate statistics
        total_courses = Course.objects.filter(section__instructor=faculty).distinct().count()
        total_students = Student.objects.filter(enrollment__section__instructor=faculty).distinct().count()
        total_sections = teaching_sections.count()
        
        # Calculate average enrollment percentage
        if total_sections > 0:
            total_enrollment_percentage = sum(
                (section.enrolled_students.count() / section.capacity) * 100 
                for section in teaching_sections
            )
            avg_enrollment = round(total_enrollment_percentage / total_sections)
        else:
            avg_enrollment = 0
        
        context = {
            'teaching_sections': teaching_sections,
            'total_courses': total_courses,
            'total_students': total_students,
            'total_sections': total_sections,
            'avg_enrollment': avg_enrollment,
        }
        return render(request, 'dashboard/faculty_dashboard.html', context)
    except Faculty.DoesNotExist:
        messages.error(request, 'Please complete your faculty profile first.')
        return redirect('users:faculty_profile')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')

@login_required
def home(request):
    """Home view that shows different content based on user role."""
    user = request.user
    
    if user.is_admin():
        return redirect('admin:index')
    elif user.is_faculty():
        return redirect('users:faculty_admin_dashboard')
    elif user.is_student():
        return redirect('users:student_dashboard')
    else:
        messages.error(request, 'Invalid user role')
        return redirect('users:login')

class Login(LoginView):
    template_name = "users/accounts/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.role == 'student':
            return reverse('users:home')
        elif user.role == 'faculty':
            return reverse('users:home')
        else:
            return reverse('users:home')  # default fallback

class RegisterUser(FormView):
    template_name = "users/accounts/register.html"
    form_class = RegisterUserForm
    success_url = "/home/"  # Not used directly because of custom redirects

    def form_valid(self, form):
        user = form.save(commit=False)
        role = form.cleaned_data.get('role')
        user.role = role
        user.save()

        if role.name.lower() == 'student':
            Student.objects.create(
                user=user,
                student_name="",
                student_last_name="",
                student_id=f"S{user.id}",
                degree_program="",
                enrollment_year=0
            )
        elif role.name.lower() == 'faculty':
            Faculty.objects.create(
                user=user,
                name="",
                last_name="",
                employee_id=f"E{user.id}",
                department="",
                title="",
                office=""
            )

        login(self.request, user)

        if user.is_student():
            return redirect("student_profile")
        elif user.is_faculty():
            return redirect("faculty_profile")
        return redirect("home")


class StudentProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = StudentProfileForm(instance=request.user.student)
        return render(request, "users/student_profile.html", {"form": form})

    def post(self, request):
        form = StudentProfileForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            return redirect("users:home")  # Updated to use correct namespace
        return render(request, "users/student_profile.html", {"form": form})


class FacultyProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = FacultyProfileForm(instance=request.user.faculty)
        return render(request, "users/faculty_profile.html", {"form": form})

    def post(self, request):
        form = FacultyProfileForm(request.POST, instance=request.user.faculty)
        if form.is_valid():
            form.save()
            return redirect("users:home")  # Updated to use correct namespace
        return render(request, "users/faculty_profile.html", {"form": form})

@login_required
def profile(request):
    """View user profile based on role."""
    user = request.user
    
    if user.is_student():
        return redirect('users:student_profile')
    elif user.is_faculty():
        return redirect('users:faculty_profile')
    else:
        messages.error(request, 'Profile not available for this user type.')
        return redirect('users:home')

@login_required
def edit_profile(request):
    """Edit user profile based on role."""
    user = request.user
    
    if user.is_student():
        return redirect('users:student_profile')
    elif user.is_faculty():
        return redirect('users:faculty_profile')
    else:
        messages.error(request, 'Profile editing not available for this user type.')
        return redirect('users:home')

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def faculty_admin_dashboard(request):
    """Admin dashboard for faculty members to manage all data."""
    # Get all data for the dashboard
    courses = Course.objects.all().select_related('department')
    sections = Section.objects.all().select_related('course', 'semester', 'instructor')
    students = Student.objects.all().select_related('user')
    faculty = Faculty.objects.all().select_related('user')
    
    context = {
        'courses': courses,
        'sections': sections,
        'students': students,
        'faculty': faculty,
    }
    
    return render(request, 'dashboard/faculty_admin.html', context)

@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.student_id = request.POST['student_id']
        student.student_name = request.POST['student_name']
        student.student_last_name = request.POST['student_last_name']
        student.user.email = request.POST['email']
        student.user.save()
        student.degree_program = request.POST['degree_program']
        student.enrollment_year = request.POST['enrollment_year']
        student.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('users:faculty_admin_dashboard')
    
    return render(request, 'users/student_edit.html', {'student': student})

@login_required
def faculty_edit(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    departments = Department.objects.all()
    
    if request.method == 'POST':
        faculty.employee_id = request.POST['employee_id']
        faculty.name = request.POST['name']
        faculty.last_name = request.POST['last_name']
        faculty.user.email = request.POST['email']
        faculty.user.save()
        faculty.department = Department.objects.get(id=request.POST['department'])
        faculty.title = request.POST['title']
        faculty.save()
        messages.success(request, 'Faculty updated successfully.')
        return redirect('dashboard:faculty_admin')
    
    return render(request, 'users/faculty_edit.html', {
        'faculty': faculty,
        'departments': departments
    })

@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.user.delete()  # This will also delete the student due to CASCADE
        messages.success(request, 'Student deleted successfully.')
        return redirect('users:faculty_admin_dashboard')
    return render(request, 'users/student_confirm_delete.html', {'student': student})

@login_required
def faculty_delete(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == 'POST':
        faculty.user.delete()  # This will also delete the faculty due to CASCADE
        messages.success(request, 'Faculty deleted successfully.')
        return redirect('dashboard:faculty_admin')
    return render(request, 'users/faculty_confirm_delete.html', {'faculty': faculty})

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def student_create(request):
    """Create a new student (faculty/admin only)."""
    if request.method == 'POST':
        # Validate input
        student_id = request.POST.get('student_id', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        degree_program = request.POST.get('degree_program', '').strip()
        enrollment_year = request.POST.get('enrollment_year', '').strip()

        # Validation checks
        errors = []
        
        # Student ID validation (format: S followed by 6 digits)
        if not student_id.startswith('S') or not student_id[1:].isdigit() or len(student_id) != 7:
            errors.append('Student ID must start with S followed by 6 digits (e.g., S000001)')
        
        # Name validation
        if not first_name or len(first_name) > 50 or not first_name.replace(' ', '').isalpha():
            errors.append('First name must be alphabetic and less than 50 characters')
        if not last_name or len(last_name) > 50 or not last_name.replace(' ', '').isalpha():
            errors.append('Last name must be alphabetic and less than 50 characters')
        
        # Email validation
        if not email or '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address')
        elif CustomUser.objects.filter(email=email).exists():
            errors.append('This email is already registered')
        
        # Degree program validation
        if not degree_program or len(degree_program) > 100:
            errors.append('Degree program must be provided and less than 100 characters')
        
        # Enrollment year validation
        try:
            enrollment_year = int(enrollment_year)
            current_year = datetime.now().year
            if enrollment_year < current_year - 5 or enrollment_year > current_year + 1:
                errors.append(f'Enrollment year must be between {current_year - 5} and {current_year + 1}')
        except ValueError:
            errors.append('Enrollment year must be a valid number')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'users/student_create.html')

        try:
            # Create the user account
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=email,  # Set initial password same as email
                first_name=first_name,
                last_name=last_name,
                role='student'
            )
            
            # Create the student profile
            student = Student.objects.create(
                user=user,
                student_id=student_id,
                student_name=first_name,
                student_last_name=last_name,
                degree_program=degree_program,
                enrollment_year=enrollment_year
            )
            
            messages.success(request, f'Student {student.student_id} created successfully.')
            return redirect('users:faculty_admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating student: {str(e)}')
            return render(request, 'users/student_create.html')
    
    return render(request, 'users/student_create.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def faculty_create(request):
    """Create a new faculty member (superuser only)."""
    departments = Department.objects.all()
    
    if request.method == 'POST':
        # Create the user account first
        user = CustomUser.objects.create_user(
            username=request.POST['email'],
            email=request.POST['email'],
            password=request.POST['password'],
            role='faculty'
        )
        
        # Create the faculty profile
        faculty = Faculty.objects.create(
            user=user,
            employee_id=request.POST['employee_id'],
            name=request.POST['name'],
            last_name=request.POST['last_name'],
            department=Department.objects.get(id=request.POST['department']),
            title=request.POST['title'],
            office=request.POST.get('office', '')
        )
        
        messages.success(request, f'Faculty member {faculty.name} {faculty.last_name} created successfully.')
        return redirect('dashboard:faculty_admin')
    
    return render(request, 'users/faculty_create.html', {
        'departments': departments
    })
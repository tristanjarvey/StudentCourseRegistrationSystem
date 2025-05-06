from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Course, Section, Prerequisite, Department, Semester, Building, Classroom
from registrations.models import Enrollment
from .forms import CourseForm
from users.models import Student, Faculty
from django.db import models

# Access control decorators
def is_faculty(user):
    return user.is_faculty()

def is_student(user):
    return user.is_student()

def is_admin(user):
    return user.is_admin()

# Faculty/Admin Views
@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def course_create(request):
    """Create a new course (faculty/admin only)."""
    departments = Department.objects.all()
    
    if request.method == 'POST':
        course = Course.objects.create(
            code=request.POST['code'],
            name=request.POST['name'],
            department=Department.objects.get(id=request.POST['department']),
            credits=request.POST['credits'],
            description=request.POST.get('description', '')
        )
        messages.success(request, f'Course {course.code} created successfully.')
        return redirect('users:faculty_admin_dashboard')
    
    return render(request, 'courses/course_create.html', {
        'departments': departments
    })

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def course_edit(request, course_id):
    """Edit an existing course (faculty/admin only)."""
    course = get_object_or_404(Course, id=course_id)
    departments = Department.objects.all()
    
    if request.method == 'POST':
        course.code = request.POST['code']
        course.name = request.POST['name']
        course.department = Department.objects.get(id=request.POST['department'])
        course.credits = request.POST['credits']
        course.description = request.POST.get('description', '')
        course.save()
        messages.success(request, 'Course updated successfully.')
        return redirect('users:faculty_admin_dashboard')
    
    return render(request, 'courses/course_edit.html', {
        'course': course,
        'departments': departments
    })

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def section_manage(request, section_id):
    """Manage a section (faculty/admin only)."""
    section = get_object_or_404(Section, id=section_id)
    enrolled_students = Enrollment.objects.filter(section=section)
    
    return render(request, 'courses/section_manage.html', {
        'section': section,
        'enrolled_students': enrolled_students
    })

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def update_grade(request, enrollment_id):
    """Update a student's grade (faculty/admin only)."""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == 'POST':
        grade = request.POST.get('grade')
        enrollment.grade = grade
        enrollment.save()
        messages.success(request, f'Grade updated for {enrollment.student.get_full_name()}')
        return redirect('courses:section_manage', section_id=enrollment.section.id)
    
    return redirect('courses:section_manage', section_id=enrollment.section.id)

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def course_delete(request, course_id):
    """Delete a course (faculty/admin only)."""
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('users:faculty_admin_dashboard')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
def section_edit(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    courses = Course.objects.all()
    semesters = Semester.objects.all()
    faculty_list = Faculty.objects.all()
    buildings = Building.objects.all()
    classrooms = Classroom.objects.all()
    
    if request.method == 'POST':
        section.section_id = request.POST['section_id']
        section.course = Course.objects.get(id=request.POST['course'])
        section.semester = Semester.objects.get(id=request.POST['semester'])
        section.instructor = Faculty.objects.get(id=request.POST['instructor'])
        section.capacity = request.POST['capacity']
        section.day = request.POST['day']
        section.time_slot = request.POST['time_slot']
        section.building = Building.objects.get(id=request.POST['building'])
        section.classroom = Classroom.objects.get(id=request.POST['classroom'])
        section.save()
        messages.success(request, 'Section updated successfully.')
        return redirect('users:faculty_admin_dashboard')
    
    return render(request, 'courses/section_edit.html', {
        'section': section,
        'courses': courses,
        'semesters': semesters,
        'faculty_list': faculty_list,
        'buildings': buildings,
        'classrooms': classrooms,
        'days': Section.DAYS_OF_WEEK,
        'time_slots': Section.TIME_SLOTS
    })

@login_required
def section_delete(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Section deleted successfully.')
        return redirect('users:faculty_admin_dashboard')
    return render(request, 'courses/section_confirm_delete.html', {'section': section})

@login_required
@user_passes_test(lambda u: is_faculty(u) or is_admin(u))
def section_create(request):
    """Create a new section (faculty/admin only)."""
    courses = Course.objects.all()
    semesters = Semester.objects.all()
    faculty_list = Faculty.objects.all()
    buildings = Building.objects.all()
    classrooms = Classroom.objects.all()
    
    if request.method == 'POST':
        section = Section.objects.create(
            section_id=request.POST['section_id'],
            course=Course.objects.get(id=request.POST['course']),
            semester=Semester.objects.get(id=request.POST['semester']),
            instructor=Faculty.objects.get(id=request.POST['instructor']),
            capacity=request.POST['capacity'],
            day=request.POST['day'],
            time_slot=request.POST['time_slot'],
            building=Building.objects.get(id=request.POST['building']),
            classroom=Classroom.objects.get(id=request.POST['classroom'])
        )
        messages.success(request, f'Section {section.section_id} created successfully.')
        return redirect('users:faculty_admin_dashboard')
    
    return render(request, 'courses/section_create.html', {
        'courses': courses,
        'semesters': semesters,
        'faculty_list': faculty_list,
        'buildings': buildings,
        'classrooms': classrooms,
        'days': Section.DAYS_OF_WEEK,
        'time_slots': Section.TIME_SLOTS
    })

# Student Views
@login_required
def my_courses(request):
    """Display courses based on user role (student enrollments or faculty teaching)."""
    if request.user.is_student():
        try:
            student = request.user.student
            # Get enrolled courses
            enrollments = Enrollment.objects.filter(student=student)
            
            # Get available sections (sections not enrolled in and with available seats)
            enrolled_section_ids = enrollments.values_list('section_id', flat=True)
            available_sections = Section.objects.exclude(
                id__in=enrolled_section_ids
            ).annotate(
                enrollment_count=models.Count('enrollment'),
                available_seats=models.ExpressionWrapper(
                    models.F('capacity') - models.F('enrollment_count'),
                    output_field=models.IntegerField()
                )
            ).filter(
                available_seats__gt=0
            ).select_related('course', 'instructor')
            
            return render(request, 'courses/student/my_courses.html', {
                'enrollments': enrollments,
                'available_sections': available_sections
            })
        except Student.DoesNotExist:
            return redirect('users:student_profile')
    elif request.user.is_faculty():
        try:
            teaching_sections = Section.objects.filter(instructor=request.user.faculty)
            return render(request, 'courses/faculty/my_courses.html', {
                'teaching_sections': teaching_sections
            })
        except Faculty.DoesNotExist:
            return redirect('users:faculty_profile')
    else:
        messages.error(request, 'Invalid user role')
        return redirect('users:home')

@login_required
def my_schedule(request):
    """Display schedule based on user role (student class schedule or faculty teaching schedule)."""
    time_slots = Section.TIME_SLOTS
    days = Section.DAYS_OF_WEEK
    
    if request.user.is_student():
        try:
            enrollments = Enrollment.objects.filter(student=request.user.student)
            return render(request, 'courses/student/my_schedule.html', {
                'enrollments': enrollments,
                'time_slots': time_slots,
                'days': days
            })
        except Student.DoesNotExist:
            return redirect('users:student_profile')
    elif request.user.is_faculty():
        try:
            teaching_sections = Section.objects.filter(instructor=request.user.faculty)
            return render(request, 'courses/faculty/my_schedule.html', {
                'teaching_sections': teaching_sections,
                'time_slots': time_slots,
                'days': days
            })
        except Faculty.DoesNotExist:
            return redirect('users:faculty_profile')
    else:
        messages.error(request, 'Invalid user role')
        return redirect('users:home')

@login_required
@user_passes_test(is_student)
def enroll(request, section_id):
    """Handle student enrollment in a section."""
    section = get_object_or_404(Section, id=section_id)
    
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('users:student_profile')
    
    # Check if student is already enrolled
    if Enrollment.objects.filter(student=student, section=section).exists():
        messages.error(request, 'You are already enrolled in this section.')
        return redirect('courses:my_courses')
    
    # Check prerequisites
    prerequisites = Prerequisite.objects.filter(course=section.course)
    for prereq in prerequisites:
        if not Enrollment.objects.filter(
            student=student,
            section__course=prereq.prerequisite,
            grade__gte='C'
        ).exists():
            messages.error(request, f'You have not completed the prerequisite for {section.course.name}')
            return redirect('courses:my_courses')
    
    # Create enrollment
    Enrollment.objects.create(
        student=student,
        section=section
    )
    messages.success(request, f'Successfully enrolled in {section.course.code} - Section {section.section_number}')
    return redirect('courses:my_courses')

@login_required
@user_passes_test(is_student)
def unenroll(request, section_id):
    """Handle student unenrollment from a section."""
    section = get_object_or_404(Section, id=section_id)
    try:
        enrollment = get_object_or_404(Enrollment, student=request.user.student, section=section)
        enrollment.delete()
        messages.success(request, f'Successfully unenrolled from {section.course.code} - Section {section.section_number}')
    except Student.DoesNotExist:
        return redirect('users:student_profile')
    return redirect('courses:my_courses')

# Common Views (accessible by all authenticated users)
@login_required
def course_list(request):
    """Display all available courses."""
    courses = Course.objects.all().order_by('department__name', 'code')
    return render(request, 'courses/course_list.html', {
        'courses': courses
    })

@login_required
def course_detail(request, course_id):
    """Display detailed information about a specific course."""
    course = get_object_or_404(Course, id=course_id)
    sections = Section.objects.filter(course=course)
    prerequisites = Prerequisite.objects.filter(course=course)
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'sections': sections,
        'prerequisites': prerequisites
    })

@login_required
def section_list(request):
    """Display all available sections."""
    sections = Section.objects.all().order_by('course__code', 'section_number')
    return render(request, 'courses/section_list.html', {
        'sections': sections
    })

@login_required
def section_detail(request, section_id):
    """Display detailed information about a specific section."""
    section = get_object_or_404(Section, id=section_id)
    enrolled_students = Enrollment.objects.filter(section=section)
    
    return render(request, 'courses/section_detail.html', {
        'section': section,
        'enrolled_students': enrolled_students
    })

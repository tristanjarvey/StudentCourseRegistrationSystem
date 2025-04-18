from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course, Enrollment

def course_registration(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student = request.user.student  # Assumes a one-to-one link between User and Student

        # Check if student already enrolled in the course
        if Enrollment.objects.filter(student=student, course_id=course_id).exists():
            messages.error(request, 'You are already enrolled in this course.')
        else:
            Enrollment.objects.create(student=student, course_id=course_id)
            messages.success(request, 'You have successfully registered for the course.')

        return redirect('course_registration')

    # Fetch current student enrollments
    enrollments = Enrollment.objects.filter(student=request.user.student).select_related('course')

    return render(request, 'registration/course_registration.html', {
        'courses': courses,
        'enrollments': enrollments,
    })

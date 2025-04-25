from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Course, Enrollment, Section
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def course_registration(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student = request.user.student

        # Check if already enrolled in the course
        if Enrollment.objects.filter(student=student, course_id=course_id).exists():
            messages.error(request, 'You are already enrolled in this course.')
        else:
            course = get_object_or_404(Course, id=course_id)

            # Select the first available section
            section = Section.objects.filter(course=course).first()

            if not section:
                messages.error(request, 'No available section for this course.')
                return redirect('registrations:course_registration')

            prerequisites = course.prerequisites.all()
            completed_courses = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)

            unmet = [prereq for prereq in prerequisites if prereq.id not in completed_courses]
            if unmet:
                messages.error(request, f"Missing prerequisites: {', '.join(str(c) for c in unmet)}")
            else:
                conflict = Enrollment.objects.filter(
                    student=student,
                    section__days=section.days,
                    section__start_time__lt=section.end_time,
                    section__end_time__gt=section.start_time
                ).exists()

                if conflict:
                    messages.error(request, "Schedule conflict detected.")
                    return redirect('registrations:course_registration')

                Enrollment.objects.create(student=student, course=course, section=section)
                messages.success(request, 'You have successfully registered for the course.')

        return redirect('registrations:course_registration')

    enrollments = Enrollment.objects.filter(student=request.user.student).select_related('course', 'section')
    return render(request, 'registrations/course_registration.html', {
        'courses': courses,
        'enrollments': enrollments,
    })

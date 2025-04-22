from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required

@login_required
def course_registration(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student = request.user.student

        if Enrollment.objects.filter(student=student, course_id=course_id).exists():
            messages.error(request, 'You are already enrolled in this course.')
        else:
            course = get_object_or_404(Course, id=course_id)
            section = Course.objects.filter(course=course).first()  # Assume we're enrolling in the first section

            # Prerequisite checking
            prerequisites = course.prerequisites.all()
            completed_courses = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)

            unmet = [prereq for prereq in prerequisites if prereq.id not in completed_courses]
            if unmet:
                messages.error(request, f"Missing prerequisites: {', '.join(str(c) for c in unmet)}")
            else:
                # Schedule conflict check logic
                conflict = Enrollment.objects.filter(
                    student=student,
                    course__section__days=section.days,
                    course__section__start_time__lt=section.end_time,
                    course__section__end_time__gt=section.start_time
                ).exists()

                if conflict:
                    messages.error(request, "Schedule conflict detected.")
                    return redirect('registrations:course_registration')

                # If no conflict, proceed with enrollment
                Enrollment.objects.create(student=student, course=course)
                messages.success(request, 'You have successfully registered for the course.')

        return redirect('registrations:course_registration')

    enrollments = Enrollment.objects.filter(student=request.user.student).select_related('course')
    return render(request, 'registrations/course_registration.html', {
        'courses': courses,
        'enrollments': enrollments,
    })
@login_required
def drop_course(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user.student)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Course dropped successfully.')
    return redirect('registrations:course_registration')


@login_required
def student_schedule(request):
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student).select_related('section__course')

    return render(request, 'registration/student_schedule.html', {
        'enrollments': enrollments,
    })

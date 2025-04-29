from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Section, Department, Semester

# View course catalog
def course_catalog(request):
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(name__icontains=query)
    else:
        courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses, 'query': query})

# View course detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

# Create a course manually
def create_course(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        code = request.POST['code']
        name = request.POST['name']
        description = request.POST.get('description', '')
        credits = request.POST['credits']
        department_id = request.POST['department']
        department = Department.objects.get(id=department_id)

        Course.objects.create(
            code=code,
            name=name,
            description=description,
            credits=credits,
            department=department
        )
        return redirect('courses:course_list')

    return render(request, 'courses/course_form.html', {'departments': departments, 'title': 'Create Course'})

# Edit course manually
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    departments = Department.objects.all()

    if request.method == 'POST':
        course.code = request.POST['code']
        course.name = request.POST['name']
        course.description = request.POST.get('description', '')
        course.credits = request.POST['credits']
        department_id = request.POST['department']
        course.department = Department.objects.get(id=department_id)
        course.save()
        return redirect('courses:course_detail', course_id=course_id)

    return render(request, 'courses/course_form.html', {'course': course, 'departments': departments, 'title': 'Edit Course'})

# Delete course
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# View sections for a course
def section_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    sections = Section.objects.filter(course=course)
    return render(request, 'courses/section_list.html', {'course': course, 'sections': sections})

# Create a section manually
def create_section(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    semesters = Semester.objects.all()

    if request.method == 'POST':
        semester_id = request.POST['semester']
        semester = Semester.objects.get(id=semester_id)
        section_number = request.POST['section_number']
        instructor = request.POST['instructor']
        schedule = request.POST['schedule']
        location = request.POST['location']

        Section.objects.create(
            course=course,
            semester=semester,
            section_number=section_number,
            instructor=instructor,
            schedule=schedule,
            location=location
        )
        return redirect('courses:section_list', course_id=course_id)

    return render(request, 'courses/section_form.html', {'course': course, 'semesters': semesters})

# Section detail
def section_detail(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    return render(request, 'courses/section_detail.html', {'section': section})

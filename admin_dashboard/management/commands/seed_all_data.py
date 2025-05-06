from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from admin_dashboard.models import Building, Classroom
from users.models import CustomUser, Faculty, Student, UserRole
from courses.models import Course, Section, Prerequisite, Semester, Department
from registrations.models import Enrollment
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample data for all models'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to seed database...')
        
        # Save superuser data if it exists
        superuser = None
        try:
            superuser = CustomUser.objects.get(username='tjjarvey')
            superuser_data = {
                'username': superuser.username,
                'email': superuser.email,
                'password': superuser.password,
                'first_name': superuser.first_name,
                'last_name': superuser.last_name,
                'is_staff': superuser.is_staff,
                'is_superuser': superuser.is_superuser,
                'role': superuser.role
            }
            self.stdout.write('Found existing superuser account.')
        except CustomUser.DoesNotExist:
            self.stdout.write('No existing superuser account found.')
        
        # Clear existing data in correct order to handle foreign key constraints
        self.stdout.write('Clearing existing data...')
        
        # First clear models with foreign key dependencies
        Enrollment.objects.all().delete()
        Prerequisite.objects.all().delete()
        Section.objects.all().delete()
        Course.objects.all().delete()
        Classroom.objects.all().delete()
        Building.objects.all().delete()
        
        # Then clear user-related models
        Student.objects.all().delete()
        Faculty.objects.all().delete()
        CustomUser.objects.all().delete()
        
        # Finally clear independent models
        Department.objects.all().delete()
        Semester.objects.all().delete()
        UserRole.objects.all().delete()
        
        self.stdout.write('Existing data cleared successfully.')
        
        # Restore superuser if it existed
        if superuser_data:
            CustomUser.objects.create(
                username=superuser_data['username'],
                email=superuser_data['email'],
                password=superuser_data['password'],
                first_name=superuser_data['first_name'],
                last_name=superuser_data['last_name'],
                is_staff=superuser_data['is_staff'],
                is_superuser=superuser_data['is_superuser'],
                role=superuser_data['role']
            )
            self.stdout.write('Superuser account restored.')
        
        # Create user roles
        self.stdout.write('Creating user roles...')
        roles = [
            UserRole.objects.create(role_id='STU', name='Student'),
            UserRole.objects.create(role_id='FAC', name='Faculty'),
            UserRole.objects.create(role_id='ADM', name='Admin'),
        ]

        # Create departments
        departments = [
            Department.objects.create(dept_id='CS', name="Computer Science"),
            Department.objects.create(dept_id='MATH', name="Mathematics"),
            Department.objects.create(dept_id='PHYS', name="Physics"),
            Department.objects.create(dept_id='CHEM', name="Chemistry"),
        ]

        # Create buildings and classrooms
        buildings = [
            Building.objects.create(building_id='EMS', name="Engineering and Math Science Building"),
            Building.objects.create(building_id='CHEM', name="Chemistry Building"),
            Building.objects.create(building_id='PHYS', name="Physics Building"),
            Building.objects.create(building_id='MITC', name="Mitchell Hall"),
        ]

        classrooms = [
            Classroom(building=buildings[0], classroom_id='EMS-E190', room_number="E190", capacity=100),
            Classroom(building=buildings[1], classroom_id='CHEM-233', room_number="233", capacity=15),
            Classroom(building=buildings[2], classroom_id='PHYS-145', room_number="145", capacity=20),
            Classroom(building=buildings[3], classroom_id='MITC-154', room_number="154", capacity=50),
        ]
        Classroom.objects.bulk_create(classrooms)

        # Create semesters
        current_year = datetime.now().year
        semesters = [
            Semester.objects.create(
                semester_id=f'F{current_year}',
                name=f"Fall {current_year}",
                start_date=datetime(current_year, 9, 1),
                end_date=datetime(current_year, 12, 20)
            ),
            Semester.objects.create(
                semester_id=f'S{current_year + 1}',
                name=f"Spring {current_year + 1}",
                start_date=datetime(current_year + 1, 1, 22),
                end_date=datetime(current_year + 1, 5, 15)
            ),
        ]

        # Create demo accounts
        # Demo faculty account
        demo_faculty_user = CustomUser.objects.create(
            username="prof.johnson",
            email="prof.johnson@university.edu",
            password=make_password("password"),
            first_name="Professor",
            last_name="Johnson",
            role=CustomUser.FACULTY
        )
        demo_faculty = Faculty.objects.create(
            user=demo_faculty_user,
            employee_id="F0001",
            name="Professor",
            last_name="Johnson",
            department=departments[0].name,  # Computer Science
            title="Associate Professor",
            office="EMS 200"
        )

        # Demo student account
        demo_student_user = CustomUser.objects.create(
            username="john.doe",
            email="john.doe@university.edu",
            password=make_password("password"),
            first_name="John",
            last_name="Doe",
            role=CustomUser.STUDENT
        )
        demo_student = Student.objects.create(
            user=demo_student_user,
            student_id="S000001",
            student_name="John",
            student_last_name="Doe",
            degree_program="Computer Science",
            enrollment_year=current_year - 1
        )

        # Create additional faculty users
        faculty_users = [demo_faculty]  # Start with demo faculty
        for i in range(1, 5):
            user = CustomUser.objects.create(
                username=f"prof{i}",
                email=f"prof{i}@uwm.edu",
                password=make_password("password123"),
                first_name=f"Professor{i}",
                last_name=f"Smith{i}",
                role=CustomUser.FACULTY
            )
            faculty = Faculty.objects.create(
                user=user,
                employee_id=f"F{i+1:04d}",
                name=f"Professor{i}",
                last_name=f"Smith{i}",
                department=departments[i % len(departments)].name,
                title="Assistant Professor",
                office=f"EMS {i}00"
            )
            faculty_users.append(faculty)

        # Create additional student users
        student_instances = [demo_student]  # Start with demo student
        for i in range(1, 11):
            user = CustomUser.objects.create(
                username=f"student{i}",
                email=f"student{i}@uwm.edu",
                password=make_password("password123"),
                first_name=f"Student{i}",
                last_name=f"Johnson{i}",
                role=CustomUser.STUDENT
            )
            student = Student.objects.create(
                user=user,
                student_id=f"S{i+1:06d}",
                student_name=f"Student{i}",
                student_last_name=f"Johnson{i}",
                degree_program="Computer Science",
                enrollment_year=current_year - random.randint(0, 3)
            )
            student_instances.append(student)

        # Create courses
        courses = [
            Course.objects.create(
                code="CS201",
                name="Introduction to Programming",
                description="Basic programming concepts and problem-solving techniques",
                credits=3,
                department=departments[0]
            ),
            Course.objects.create(
                code="CS251",
                name="Data Structures",
                description="Study of fundamental data structures and algorithms",
                credits=3,
                department=departments[0]
            ),
            Course.objects.create(
                code="CS351",
                name="Database Systems",
                description="Design and implementation of database systems",
                credits=3,
                department=departments[0]
            ),
            Course.objects.create(
                code="MATH231",
                name="Calculus I",
                description="Introduction to differential and integral calculus",
                credits=4,
                department=departments[1]
            ),
        ]

        # Create prerequisites
        Prerequisite.objects.create(
            course=courses[1],  # Data Structures
            prerequisite=courses[0]  # Intro to Programming
        )
        Prerequisite.objects.create(
            course=courses[2],  # Database Systems
            prerequisite=courses[1]  # Data Structures
        )

        # Define possible day and time combinations
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        time_slots = ['08:00-09:15', '09:30-10:45', '11:00-12:15', '12:30-13:45', '14:00-15:15', '15:30-16:45']

        # Create sections
        sections = []
        for course in courses:
            for semester in semesters:
                faculty = random.choice(faculty_users)
                building = random.choice(buildings)
                classroom = random.choice(classrooms)
                day = random.choice(days)
                time_slot = random.choice(time_slots)
                
                section = Section.objects.create(
                    course=course,
                    semester=semester,
                    section_id=f"{course.code}-{semester.semester_id}01",  # e.g., "CS201-F202501"
                    section_number=f"{course.code}{semester.name[:1]}01",  # e.g., "CS201F01"
                    instructor=faculty,
                    day=day,
                    time_slot=time_slot,
                    building=building,
                    classroom=classroom,
                    capacity=classroom.capacity
                )
                sections.append(section)

        # Create enrollments
        for section in sections:
            # Randomly enroll 2-5 students in each section
            num_enrollments = random.randint(2, 5)
            # Make sure we don't try to enroll more students than we have
            num_enrollments = min(num_enrollments, len(student_instances))
            for student in random.sample(student_instances, num_enrollments):
                Enrollment.objects.create(
                    enrollment_id=f"{student.student_id}-{section.section_number}",  # e.g., "S000001-CS201F01"
                    student=student,
                    section=section
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!')) 
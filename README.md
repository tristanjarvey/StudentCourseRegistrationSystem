# Student Course Registration System (SCRS)

## Project Overview

The **Student Course Registration System (SCRS)** is a comprehensive web-based application designed to streamline the course registration process for students and course management for faculty and administrators. Built using **Django**, this application provides role-based access and features for different user types:

- **Student Features:**

  - User authentication and profile management
  - View available courses and course details
  - Register for courses and view personal schedules
  - Drop courses and manage enrollments
  - View course prerequisites and requirements
  - Track academic progress

- **Faculty Features:**

  - Manage teaching schedule and course sections
  - View enrolled students and class rosters
  - Track course enrollment statistics
  - Update course information and prerequisites

- **Administrator Features:**
  - Manage courses, sections, and faculty assignments
  - View and override student enrollments
  - View enrollment statistics and class rosters
  - Manage buildings and classrooms
  - Create and manage departments
  - Handle semester scheduling

## Technologies Used

- **Backend:**

  - Django 5.1.7 (Python)
  - Django Authentication System
  - Django Admin Interface

- **Frontend:**

  - HTML5
  - CSS3 (Bootstrap 5)
  - JavaScript
  - Django Templates

- **Database:**

  - MySQL

- **Development Tools:**
  - Git/GitHub
  - Jira
  - Python Virtual Environment

## Setup Instructions

### Prerequisites

- Python 3.x
- MySQL
- Git
- Virtual Environment (recommended)

### Installation Steps

1. Clone the repository:

   ```bash
   git clone [repository-url]
   cd StudentCourseRegistrationSystem
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure MySQL database:

   - Create a new MySQL database
   - Update database settings in `settings.py`

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Seed the database with sample data:

   ```bash
   python manage.py seed_all_data
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Database Seeding

The application includes comprehensive data seeding capabilities:

```bash
python manage.py seed_all_data
```

This command will:

- Clear existing data (while preserving superuser accounts)
- Create user roles (Student, Faculty, Admin)
- Add sample departments
- Create buildings and classrooms
- Set up current and next semester
- Create demo accounts for testing
- Add sample courses with prerequisites
- Create course sections
- Generate sample enrollments

Demo accounts are created with the following credentials:

- Student: john.doe@university.edu / (password defined in .env)
- Faculty: prof.johnson@university.edu / (password defined in .env)

## Contributing

1. Clone the repository
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Stage all changes:
   ```bash
   git add .
   ```
4. Commit your changes:
   ```bash
   git commit -m "Add your commit message here"
   ```
5. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a Pull Request (PR) for review

## Team Members

- Tristan Jarvey
- Ishika Patel
- Angel Ortiz
- Jumana Adams

# Student Course Registration System (SCRS)

## Project Overview

The **Student Course Registration System (SCRS)** is a web-based application designed to streamline the course registration process for students and course management for administrators. Built using **Django**, this application provides the following features:

- **Student Features:**

  - User authentication (login/logout).
  - View available courses and course details.
  - Register for courses and view personal schedules.
  - Drop courses and manage enrollments.

- **Administrator Features:**

  - Manage courses, sections, and faculty assignments.
  - View and override student enrollments.
  - Generate enrollment reports.

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Version Control:** Git/GitHub
- **Project Management:** Jira

## Setup Instructions

### Prerequisites

- **Python 3.x**
- **MySQL**
- **Git**

## Admin Dashboard (admin_dashboard)

### Seeding Data for admin_dashboard

To load sample buildings and classrooms into your local database, run:

> python manage.py seed_admin_data

This command will:

- Clear all existing classrooms and buildings
- Add 4 buildings and 4 classrooms
- Use this to test course scheduling, availability, etc.

You can find the script here:
admin_dashboard/management/commands/seed_data.py

## Documentation

- ER Diagrams: Located in docs/er_diagrams/.
- Project Report: Located in docs/project_report.pdf.
- User Guide: Located in docs/user_guide.md.

## Contributing

1. Clone the repository.
2. Create a new branch for your feature or bug fix:
   > git checkout -b feature/your-feature-name
3. Stage all changes:
   > git add .
4. Commit your changes:
   > git commit -m "Add your commit message here"
5. Push to the branch:
   > git push origin feature/your-feature-name
6. Create a Pull Request (PR) for review.

## Team Members

- Tristan Jarvey
- Ishika Patel
- Angel Ortiz
- Jumana Adams

# API Endpoints Reference

## Authentication
- `GET/POST /` → Login page
- `POST /login/` → User login (credentials required)
- `POST /logout/` → User logout
- `GET/POST /password-reset/` → Request password reset
- `GET/POST /set-password/` → Change password

## Dashboards
- `GET /dashboard/admin/` → Admin dashboard (admin only)
- `GET /dashboard/teacher/` → Teacher dashboard (teacher only)
- `GET /dashboard/student/` → Student dashboard (student only)

## Student Management
- `GET /students/` → List all students (with search & filter)
- `GET/POST /students/create/` → Create new student
- `GET /students/<id>/` → View student details
- `GET/POST /students/<id>/edit/` → Edit student record
- `GET/POST /students/<id>/delete/` → Deactivate student

## Teacher Management
- `GET /teachers/` → List all teachers (with search)
- `GET/POST /teachers/create/` → Create new teacher
- `GET /teachers/<id>/` → View teacher details
- `GET/POST /teachers/<id>/edit/` → Edit teacher record
- `GET/POST /teachers/<id>/delete/` → Deactivate teacher

## Class Management
- `GET /academics/classes/` → List all classes
- `GET/POST /academics/classes/create/` → Create new class
- `GET/POST /academics/classes/<id>/edit/` → Edit class

## Subject Management
- `GET /academics/subjects/` → List all subjects
- `GET/POST /academics/subjects/create/` → Create new subject
- `GET/POST /academics/subjects/<id>/edit/` → Edit subject

## Results & Grades
- `GET /academics/results/` → List all results
- `GET/POST /academics/results/create/` → Record new result
- `GET/POST /academics/results/<id>/edit/` → Edit result
- `GET /academics/report-card/<student_id>/` → View report card

## Attendance
- `GET /attendance/` → List attendance records
- `GET/POST /attendance/mark/` → Mark single attendance
- `GET/POST /attendance/bulk-mark/` → Bulk mark attendance
- `GET /attendance/report/` → View attendance report
- `GET /attendance/student/<student_id>/report/` → Student attendance report

## Django Admin
- `GET /admin/` → Django admin interface

---

## Response Patterns

### Success
- Redirects to list view with success message
- Forms re-rendered with saved data

### Error
- Form re-displayed with error messages
- User remains on the form page

### Authorization
- Non-authenticated users → redirected to login
- Insufficient permissions → 403 error page

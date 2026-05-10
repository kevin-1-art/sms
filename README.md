# School Management System (MVP)

A comprehensive, responsive Django-based School Management System with role-based access control (Admin, Teacher, Student).

## 📋 Features

### Core Modules
- **User Authentication & Roles**: Secure login/logout with role-based access control
- **Student Management**: CRUD operations, search, filter, and detailed profiles
- **Teacher Management**: Employee records, subject/class assignments
- **Class & Subject Management**: Create and manage classes and subjects
- **Attendance Module**: Daily attendance marking with bulk operations
- **Results/Grades Module**: Input marks, auto-calculate grades, view report cards
- **Dashboards**: Role-specific dashboards for Admin, Teacher, and Student

### Technical Features
- ✅ Responsive Bootstrap 5 UI (Mobile-first design)
- ✅ SQLite database with Django ORM
- ✅ Role-based access control with decorators
- ✅ Clean MVC architecture with separate Django apps
- ✅ Django Admin integration
- ✅ Form validation and error handling
- ✅ Print-friendly report cards

## 🏗️ Project Structure

```
school_management/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── init_db.py                        # Database initialization script
├── config/                           # Project configuration
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Main URL routing
│   └── wsgi.py                       # WSGI configuration
├── apps/                             # Django applications
│   ├── users/                        # Authentication & User management
│   │   ├── models.py                # CustomUser model with roles
│   │   ├── views.py                 # Login, logout, password reset
│   │   ├── forms.py                 # Authentication forms
│   │   ├── admin.py                 # Django admin configuration
│   │   ├── urls.py                  # User app URLs
│   │   └── dashboard_views.py       # Dashboard views for each role
│   ├── students/                     # Student management
│   │   ├── models.py                # Student model
│   │   ├── views.py                 # CRUD operations
│   │   ├── forms.py                 # Student forms
│   │   └── urls.py
│   ├── teachers/                     # Teacher management
│   │   ├── models.py                # Teacher model with assignments
│   │   ├── views.py                 # Teacher CRUD
│   │   ├── forms.py
│   │   └── urls.py
│   ├── academics/                    # Classes, Subjects, Results
│   │   ├── models.py                # Class, Subject, Result models
│   │   ├── views.py                 # Academic management views
│   │   ├── forms.py
│   │   └── urls.py
│   └── attendance/                   # Attendance management
│       ├── models.py                # Attendance, AttendanceSummary
│       ├── views.py                 # Attendance marking and reports
│       ├── forms.py
│       └── urls.py
├── templates/                        # HTML templates (Bootstrap 5)
│   ├── base/
│   │   └── base.html                # Base template with sidebar navigation
│   ├── users/
│   │   ├── login.html
│   │   ├── password_reset.html
│   │   └── set_password.html
│   ├── dashboard/
│   │   ├── admin_dashboard.html
│   │   ├── teacher_dashboard.html
│   │   └── student_dashboard.html
│   ├── students/
│   │   ├── student_list.html
│   │   ├── student_form.html
│   │   ├── student_detail.html
│   │   └── student_confirm_delete.html
│   ├── teachers/                    # Similar structure to students
│   ├── academics/                   # Class, Subject, Result templates
│   └── attendance/                  # Attendance templates
├── static/
│   ├── css/                         # Custom CSS (if needed)
│   └── js/                          # Custom JavaScript
└── media/                           # User uploads (profile pictures, etc.)
```

## 🔐 User Roles & Permissions

### Admin
- View dashboards with system statistics
- Manage all students, teachers, classes, subjects
- View all attendance and results
- Access Django Admin panel

### Teacher
- View assigned classes and subjects
- Mark and view attendance
- Record student marks/grades
- View attendance reports

### Student
- View personal dashboard
- Check attendance records
- View grades and report card
- View personal profile

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd school_management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Create database tables
python manage.py migrate

# Initialize database with sample data
python init_db.py
```

### Step 4: Create Admin Account (Optional)

```bash
python manage.py createsuperuser
# Follow prompts to create an admin account
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## 📝 Sample Login Credentials

After running `init_db.py`:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | teacher1 | teacher123 |
| Student | student1 | student123 |

## 🎨 UI/UX Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Bootstrap 5**: Modern, clean, and professional styling
- **Sidebar Navigation**: Fixed sidebar with role-based menu options
- **Status Indicators**: Color-coded badges for status (Present/Absent, Grades)
- **Statistical Cards**: Quick statistics on dashboards
- **Print-Friendly**: Report cards can be printed directly from the browser
- **Form Validation**: Real-time validation with user-friendly error messages

## 📊 Database Models

### Users
- CustomUser (extends Django User with role and profile fields)

### Students
- Student (name, admission number, class, guardian info, DOB)
- Attendance (daily records with Present/Absent/Leave status)
- Result (marks, grades, term, academic year)

### Teachers
- Teacher (employee ID, qualification, assigned subjects/classes)

### Academics
- Class (class level, section, capacity, class teacher)
- Subject (name, code, description)
- SubjectClass (link between subjects and classes)
- Result (student marks and grades)

## 🔄 Workflow Examples

### Adding a Student
1. Admin → Students → Add New Student
2. Fill in student details (name, admission number, gender, DOB, guardian info)
3. Assign to a class
4. System auto-creates user account with default credentials

### Marking Attendance
1. Teacher → Mark Attendance (Bulk)
2. Select class, date, and subject
3. Mark Present/Absent/Leave for each student
4. Save records

### Recording Grades
1. Teacher → Enter Grades
2. Select student, subject, marks (0-100)
3. Grade auto-calculates based on marks
4. Save result

### Viewing Report Card (Student)
1. Student → My Grades
2. View grades by term
3. Print report card

## 🛠️ Django Admin

Access Django Admin panel at: `http://127.0.0.1:8000/admin/`

Use this for:
- Direct database management
- Bulk operations
- Advanced filtering and search
- System configuration

## 📱 Responsive Features

- **Mobile Navigation**: Touch-friendly buttons and menus
- **Flexible Tables**: Responsive tables that stack on small screens
- **Form Layout**: Single-column layout on mobile, multi-column on desktop
- **Print Optimization**: Special styles for printing reports

## 🔐 Security Features

- Django CSRF protection on all forms
- Password hashing with Django's built-in system
- Role-based access control with @login_required decorators
- Session-based authentication
- SQL injection protection (ORM-based queries)

## 📈 Performance Considerations

- Database indexing on frequently queried fields
- Query optimization with select_related() and prefetch_related()
- Pagination ready (can be added to list views)
- Static file serving with whitenoise (production ready)

## 🚢 Production Deployment

### Before Deploying:
1. Set `DEBUG = False` in settings.py
2. Update `SECRET_KEY` with a secure random value
3. Set `ALLOWED_HOSTS` to your domain
4. Use PostgreSQL instead of SQLite
5. Configure environment variables using python-decouple

### Deployment Options:
- Heroku
- PythonAnywhere
- AWS (EC2, Elastic Beanstalk)
- DigitalOcean
- Google Cloud Platform

## 📚 API Endpoints

### Authentication
- `GET/POST /login/` - User login
- `POST /logout/` - User logout
- `GET/POST /password-reset/` - Password reset
- `GET/POST /set-password/` - Change password

### Dashboard
- `GET /dashboard/admin/` - Admin dashboard
- `GET /dashboard/teacher/` - Teacher dashboard
- `GET /dashboard/student/` - Student dashboard

### Students
- `GET /students/` - List students
- `POST /students/create/` - Create student
- `GET /students/<id>/` - View student details
- `GET/POST /students/<id>/edit/` - Edit student
- `GET/POST /students/<id>/delete/` - Delete student

### Similar endpoints exist for Teachers, Classes, Subjects, Attendance, and Results

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### Database Locked Error
```bash
rm db.sqlite3
python manage.py migrate
python init_db.py
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

## 📞 Support & Documentation

For Django documentation: https://docs.djangoproject.com/
For Bootstrap documentation: https://getbootstrap.com/docs/

## 📄 License

This project is provided as-is for educational and commercial use.

## ✨ Future Enhancements

- [ ] Export reports to PDF
- [ ] Email notifications
- [ ] File uploads (student photos)
- [ ] SMS notifications for parents
- [ ] Advanced analytics and reporting
- [ ] REST API for mobile apps
- [ ] Two-factor authentication
- [ ] Audit logging
- [ ] Bulk import/export CSV

---

**Happy Teaching & Learning! 🎓**

For questions or issues, refer to the code comments and Django documentation.

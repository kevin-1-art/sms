# 🎓 School Management System - Quick Start Guide

## ⚡ 30-Second Setup

```bash
# 1. Navigate to project
cd school_management

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate
python init_db.py

# 5. Run server
python manage.py runserver
```

**Access at: http://127.0.0.1:8000/login**

---

## 🔑 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| 👨‍💼 Admin | `admin` | `admin123` |
| 👨‍🏫 Teacher | `teacher1` | `teacher123` |
| 👨‍🎓 Student | `student1` | `student123` |

---

## 📱 Quick Actions

### For Admins
- **Dashboard**: See system statistics
- **Add Student**: Students → Add New Student
- **Add Teacher**: Teachers → Add New Teacher
- **Create Class**: Academics → Classes → Create New Class
- **Create Subject**: Academics → Subjects → Add New Subject

### For Teachers
- **Mark Attendance**: Mark Attendance → Bulk Mark
- **Enter Grades**: Enter Grades → Record Result
- **View Reports**: Reports section

### For Students
- **Check Attendance**: My Attendance
- **View Grades**: My Grades / Report Card
- **Update Profile**: Change Password

---

## 🏛️ Admin Panel

**URL**: http://127.0.0.1:8000/admin/

Use Django Admin for:
- Direct database management
- Bulk operations
- Advanced configuration
- Superuser management

---

## 📊 Key Views & URLs

```
/ → Login Page
/dashboard/admin/ → Admin Dashboard
/dashboard/teacher/ → Teacher Dashboard
/dashboard/student/ → Student Dashboard

/students/ → Student Management
/teachers/ → Teacher Management
/academics/classes/ → Class Management
/academics/subjects/ → Subject Management
/academics/results/ → Grades Management
/attendance/ → Attendance Records
/attendance/bulk-mark/ → Bulk Attendance
```

---

## 🎨 UI Highlights

- ✅ **Responsive Design** - Works on mobile, tablet, desktop
- ✅ **Bootstrap 5** - Modern, clean interface
- ✅ **Color-Coded Status** - Green (Present), Red (Absent), Yellow (Leave)
- ✅ **Dashboard Cards** - Quick statistics and shortcuts
- ✅ **Print Reports** - Print-friendly report cards

---

## 🔧 Common Tasks

### Add a New Student
1. Admin → Students → Add New Student
2. Fill in: Name, Admission Number, DOB, Guardian Info
3. Select Class → Save
4. Student account auto-created

### Mark Attendance (Bulk)
1. Teacher → Mark Attendance → Bulk Mark
2. Select Class, Date
3. Select Present/Absent/Leave for each student
4. Save

### Record Student Marks
1. Teacher → Enter Grades
2. Select Student, Subject, Class
3. Enter Marks (0-100) → Grade auto-calculated
4. Save

### Generate Report Card
1. Student → My Grades
2. View grades by term
3. Click Print to get PDF

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `python manage.py runserver 8001` |
| Module not found | `pip install -r requirements.txt` |
| Database locked | Delete `db.sqlite3`, run migrate again |
| Static files missing | `python manage.py collectstatic --noinput` |

---

## 🚀 Next Steps

1. **Create Classes** - Set up academic structure
2. **Add Subjects** - Define curriculum subjects
3. **Add Teachers** - Onboard teaching staff
4. **Assign Classes** - Link teachers to classes
5. **Enroll Students** - Add student records
6. **Start Attendance** - Begin daily marking
7. **Record Grades** - Input assessment marks

---

## 📚 Project Structure Basics

```
school_management/
├── apps/                  # Django applications (users, students, etc.)
├── templates/            # HTML files with Bootstrap 5
├── config/              # Django settings & URL routing
├── manage.py            # Django command script
├── init_db.py          # Sample data initialization
└── requirements.txt     # Python dependencies
```

---

## 💡 Pro Tips

- **Tip 1**: Use bulk attendance marking for faster entry
- **Tip 2**: Export to PDF by clicking print on report cards
- **Tip 3**: Use Django Admin for bulk operations
- **Tip 4**: Create classes BEFORE adding students
- **Tip 5**: Assign subjects to classes before marking attendance

---

## 📖 Additional Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Bootstrap 5**: https://getbootstrap.com/
- **SQLite Docs**: https://www.sqlite.org/docs.html

---

**Happy Managing! 🎓**

For more help, check README.md or view code comments.

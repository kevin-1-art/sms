# 🆘 Troubleshooting & FAQ

## Common Issues & Solutions

### 1. ModuleNotFoundError: No module named 'django'

**Error Message:**
```
ModuleNotFoundError: No module named 'django'
```

**Causes:**
- Virtual environment not activated
- Requirements not installed
- Wrong Python version

**Solutions:**

✅ **Activate Virtual Environment First:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

✅ **Install Requirements:**
```bash
pip install -r requirements.txt
```

✅ **Verify Django Installation:**
```bash
python -m django --version
```

---

### 2. Database Error: "database is locked"

**Error Message:**
```
sqlite3.OperationalError: database is locked
```

**Causes:**
- Multiple processes accessing database
- Incomplete migration
- Corrupted database file

**Solutions:**

✅ **Delete and Reinitialize:**
```bash
# Stop the server (Ctrl+C)
rm db.sqlite3
python manage.py migrate
python init_db.py
python manage.py runserver
```

✅ **Check for Running Processes:**
```bash
# Make sure only one Django instance is running
# Check taskbar/system processes
```

---

### 3. Port 8000 Already in Use

**Error Message:**
```
Address already in use
```

**Causes:**
- Django server already running in another terminal
- Another application using port 8000
- Previous server not properly shut down

**Solutions:**

✅ **Use Different Port:**
```bash
python manage.py runserver 8001
```

✅ **Find Process Using Port (Windows):**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

✅ **Find Process Using Port (macOS/Linux):**
```bash
lsof -i :8000
kill -9 <PID>
```

---

### 4. Static Files Not Loading (CSS, JS, Icons)

**Symptoms:**
- Page looks unstyled
- No Bootstrap styling
- Icons missing

**Causes:**
- STATIC_URL not configured
- Static files not collected
- Browser cache

**Solutions:**

✅ **Collect Static Files:**
```bash
python manage.py collectstatic --noinput
```

✅ **Check settings.py:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

✅ **Clear Browser Cache:**
- Press Ctrl+Shift+Delete (Windows/Linux)
- Press Cmd+Shift+Delete (macOS)
- Or: Right-click → Inspect → Network → disable cache

---

### 5. Templates Not Found / TemplateDoesNotExist

**Error Message:**
```
TemplateDoesNotExist: login.html
```

**Causes:**
- Wrong template path
- Missing templates directory
- TEMPLATES setting incorrect

**Solutions:**

✅ **Verify Template Directory:**
```bash
# Should exist:
templates/
├── base/
├── users/
├── dashboard/
└── ...
```

✅ **Check settings.py TEMPLATES:**
```python
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    ...
}]
```

---

### 6. Login Page Blank / No Styling

**Causes:**
- Bootstrap CDN not loading
- Internet connection issue
- Browser compatibility

**Solutions:**

✅ **Check Internet Connection:**
- Bootstrap 5 loaded via CDN
- Requires active internet

✅ **Try Different Browser:**
- Chrome
- Firefox
- Edge

✅ **Check Browser Console:**
- Press F12 → Console tab
- Look for network errors

---

### 7. Migration Errors / "Table Already Exists"

**Error Message:**
```
Error creating table: table already exists
```

**Causes:**
- Migrations out of sync
- Duplicate migration files
- Incomplete previous migration

**Solutions:**

✅ **Reset Migrations (Development Only):**
```bash
# Delete db.sqlite3
rm db.sqlite3

# Run migrations fresh
python manage.py migrate --fake

# Or reinitialize
python manage.py migrate
python init_db.py
```

✅ **Check Migration Status:**
```bash
python manage.py showmigrations
```

---

### 8. "ModuleNotFoundError: No module named 'apps'"

**Error Message:**
```
ModuleNotFoundError: No module named 'apps'
```

**Causes:**
- Wrong working directory
- Python path issue
- Missing __init__.py

**Solutions:**

✅ **Verify You're in Project Root:**
```bash
# Correct structure:
school_management/
├── manage.py
├── config/
└── apps/
```

✅ **Run from Project Root:**
```bash
cd school_management
python manage.py runserver
```

✅ **Check __init__.py Files Exist:**
- `apps/__init__.py`
- `apps/users/__init__.py`
- `apps/students/__init__.py`
- etc.

---

### 9. Login Fails / Wrong Credentials

**Symptoms:**
- "Invalid username or password" error
- Can't login as admin

**Solutions:**

✅ **Verify Credentials:**
```
Admin: username: admin | password: admin123
Teacher: username: teacher1 | password: teacher123
Student: username: student1 | password: student123
```

✅ **Create New Admin User:**
```bash
python manage.py createsuperuser
# Follow prompts to set username/password
```

✅ **Reset Password (Django Admin):**
```bash
# Access: http://127.0.0.1:8000/admin/
# Users section → select user → change password
```

---

### 10. Python Version Error

**Error Message:**
```
SyntaxError: invalid syntax
```

**Causes:**
- Python < 3.8
- Wrong Python interpreter

**Solutions:**

✅ **Check Python Version:**
```bash
python --version
# Should be 3.8 or higher
```

✅ **Use Python 3:**
```bash
python3 -m venv venv
python3 manage.py runserver
```

---

### 11. No Module Named 'Pillow'

**Error Message:**
```
ModuleNotFoundError: No module named 'PIL'
```

**Causes:**
- Pillow not installed
- Requirements not fully installed

**Solutions:**

✅ **Install Pillow:**
```bash
pip install Pillow==10.1.0
```

✅ **Reinstall All Requirements:**
```bash
pip install -r requirements.txt --force-reinstall
```

---

### 12. Images Not Displaying

**Symptoms:**
- Profile pictures show as broken image
- Media files not found

**Causes:**
- Media directory not configured
- File upload path wrong
- Files not saved to correct location

**Solutions:**

✅ **Check MEDIA Configuration in settings.py:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

✅ **Create Media Directory:**
```bash
mkdir media
```

✅ **Ensure URL Pattern in urls.py:**
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

### 13. Form Not Submitting / POST Error

**Symptoms:**
- Form reloads without saving
- Validation errors appear

**Causes:**
- Missing CSRF token
- Form validation failing
- Database constraint violation

**Solutions:**

✅ **Check for {% csrf_token %} in Forms:**
```html
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

✅ **Check Form Validation Errors:**
- Look at error messages displayed on form
- Check Django console for validation details

✅ **Check Unique Constraints:**
- Admission numbers must be unique
- Employee IDs must be unique
- Emails must be unique

---

### 14. Permission Denied / 403 Error

**Symptoms:**
- "Access Denied" message
- Redirect to 403 page
- Can't access certain pages

**Causes:**
- Wrong user role
- Not logged in
- Insufficient permissions

**Solutions:**

✅ **Ensure Logged In:**
- Check if session cookie exists
- Try logging out and back in

✅ **Check User Role:**
- Admin can access all pages
- Teachers limited to teacher pages
- Students limited to student pages

✅ **Verify Permissions in View:**
- Check view code for role requirements
- May need to be assigned to class/subject

---

### 15. Django Admin Not Accessible

**Symptoms:**
- Can't access /admin/
- Admin page shows error

**Causes:**
- Admin app not in INSTALLED_APPS
- Migrations not run
- Admin not registered

**Solutions:**

✅ **Check INSTALLED_APPS in settings.py:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',  # Must be present
    'django.contrib.auth',
    'django.contrib.contenttypes',
    ...
]
```

✅ **Run Migrations:**
```bash
python manage.py migrate
```

✅ **Access Admin:**
```
http://127.0.0.1:8000/admin/
```

---

## Frequently Asked Questions (FAQ)

### Q: Can I use PostgreSQL instead of SQLite?

**A:** Yes! SQLite is the default for MVP, but you can switch to PostgreSQL:

```bash
# 1. Install psycopg2
pip install psycopg2-binary

# 2. Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'school_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 3. Run migrations
python manage.py migrate
python init_db.py
```

---

### Q: How do I add more roles (Principal, Accountant)?

**A:** Extend CustomUser model:

```python
# apps/users/models.py
ROLE_CHOICES = [
    ('admin', 'Administrator'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('principal', 'Principal'),  # New role
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def is_principal(self):
        return self.role == 'principal'
```

---

### Q: How do I customize the color scheme?

**A:** Edit CSS in templates or override Bootstrap:

```html
<!-- In base.html -->
<style>
    :root {
        --bs-primary: #your-color;
        --bs-secondary: #your-color;
    }
</style>
```

---

### Q: Can I add file uploads?

**A:** Yes! Pillow is already included:

```python
# models.py
class Student(models.Model):
    ...
    photo = models.ImageField(upload_to='students/', blank=True)
```

---

### Q: How do I export data to Excel?

**A:** Use django-import-export:

```bash
pip install django-import-export
```

Then update admin.py to use ImportExportModelAdmin.

---

### Q: How do I send email notifications?

**A:** Configure email in settings.py:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

---

### Q: How do I backup the database?

**A:** Simple backup for SQLite:

```bash
# Copy the database file
cp db.sqlite3 db.sqlite3.backup

# Or use Django dumpdata
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

---

### Q: Can I run this on a production server?

**A:** Yes, but follow these steps:

1. **Set DEBUG = False**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Change SECRET_KEY**
   ```python
   SECRET_KEY = 'generate-random-key'
   ```

3. **Use PostgreSQL** (not SQLite)

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

5. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn config.wsgi
   ```

6. **Use NGINX as reverse proxy**

---

### Q: How do I add two-factor authentication?

**A:** Use django-otp:

```bash
pip install django-otp
```

Then follow django-otp documentation.

---

### Q: How do I create API endpoints?

**A:** Use Django REST Framework:

```bash
pip install djangorestframework
```

Create serializers and viewsets for API.

---

### Q: How do I test the application?

**A:** Create tests in each app:

```bash
# Run tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

### Q: Can I use this on Windows/Mac/Linux?

**A:** Yes! Tested and works on all platforms.

**Windows-specific:**
- Use `venv\Scripts\activate` (not `source`)
- May need to use `py` instead of `python`

**macOS/Linux:**
- Use `source venv/bin/activate`
- May need `python3` instead of `python`

---

## Getting Help

### Resources
1. **Django Documentation**: https://docs.djangoproject.com/
2. **Bootstrap 5 Docs**: https://getbootstrap.com/
3. **Stack Overflow**: Tag questions with `django`
4. **Django Community**: https://www.djangoproject.com/community/

### Before Asking for Help
1. ✅ Check this troubleshooting guide
2. ✅ Read error message carefully
3. ✅ Google the error message
4. ✅ Check Django documentation
5. ✅ Look at code comments
6. ✅ Check terminal output for clues

---

## Common Django Commands

```bash
# Project Management
python manage.py startapp appname              # Create new app
python manage.py runserver                    # Run development server
python manage.py shell                        # Django Python shell
python manage.py dbshell                      # Database shell

# Database
python manage.py migrate                      # Apply migrations
python manage.py makemigrations               # Create migration files
python manage.py migrate --fake               # Mark as migrated without running
python manage.py dumpdata > backup.json       # Backup database
python manage.py loaddata backup.json         # Restore database
python manage.py flush                        # Clear database (keep migrations)

# Admin
python manage.py createsuperuser              # Create admin user
python manage.py changepassword username      # Change user password

# Static Files
python manage.py collectstatic                # Collect static files
python manage.py findstatic filename          # Find static file

# Testing
python manage.py test                         # Run tests
python manage.py test appname                 # Test specific app

# Maintenance
python manage.py check                        # Check project for issues
python manage.py clean_sessions               # Clean expired sessions
```

---

## Performance Tips

1. **Use select_related() for ForeignKey**
2. **Use prefetch_related() for reverse relations**
3. **Index frequently searched fields**
4. **Use pagination on large lists**
5. **Cache static files**
6. **Use database indexing**
7. **Monitor slow queries** (DEBUG = True shows query time)
8. **Consider read replicas** for large scale

---

**Still stuck? 🤔**

Check the README.md for more information or review the code comments in the relevant files.

**Happy Teaching! 🎓**

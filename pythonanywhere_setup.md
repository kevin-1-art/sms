# PythonAnywhere Deployment Guide

## Quick Setup Steps

### 1. Create Account & Web App
- Sign up at https://www.pythonanywhere.com/
- Create a Django web app (Python 3.9+)
- Your initial URL will be: `yourusername.pythonanywhere.com`

### 2. Clone Your Repository
In PythonAnywhere's Bash Console:

```bash
cd ~
git clone https://github.com/kevin-1-art/sms.git
cd sms
```

### 3. Install Dependencies
```bash
mkvirtualenv --python=/usr/bin/python3.9 sms
pip install -r requirements.txt
```

### 4. Set Up Django
```bash
python manage.py migrate
python init_db.py
python manage.py collectstatic --noinput
```

### 5. Configure Web App

1. Go to **Web** → Click your app
2. **Virtualenv path:** `/home/yourusername/.virtualenvs/sms`
3. **Working directory:** `/home/yourusername/sms`
4. **WSGI file path:** Edit it (see below)

### 6. Update WSGI Configuration

Edit the WSGI file at: `/home/yourusername/var/www/yourusername_pythonanywhere_com_wsgi.py`

Replace with:
```python
import os
import sys

path = '/home/yourusername/sms'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7. Configure Static Files

In Web app settings, add this static file mapping:
- **URL:** `/static/`
- **Directory:** `/home/yourusername/sms/static`

### 8. Reload Web App

Click the **Reload** button in the Web tab.

## Access Your App

Your app will be available at: `https://yourusername.pythonanywhere.com`

## Default Login

- **Username:** ADMIN
- **Password:** admin123

## Troubleshooting

If you get errors:
1. Check **Error log** in Web tab
2. Check **Server log** in Web tab
3. Verify file paths are correct
4. Ensure `DEBUG = True` during setup (change to False for production)

#!/bin/bash
# PythonAnywhere Deployment Script for TSURI SMS

set -e

cd ~

# Clone the GitHub repository
if [ ! -d "sms" ]; then
    echo "Cloning GitHub repository..."
    git clone https://github.com/kevin-1-art/sms.git
fi

cd sms

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.9 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Update WSGI file
echo "Updating WSGI configuration..."
cat > /var/www/kevinnotoro_pythonanywhere_com_wsgi.py << 'EOF'
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = '/home/kevinnotoro/sms'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Setup Django
import django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF

echo "Deployment complete! Visit https://kevinnotoro.pythonanywhere.com"
echo "Login with: ADMIN / admin123"

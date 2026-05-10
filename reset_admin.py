#!/usr/bin/env python
"""Reset admin credentials"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing admin users
User.objects.filter(username__in=['admin', 'ADMIN']).delete()

# Create new admin user
User.objects.create_superuser(username='ADMIN', email='admin@school.local', password='admin123')

print("✅ Admin user created/reset successfully!")
print("Username: ADMIN")
print("Password: admin123")

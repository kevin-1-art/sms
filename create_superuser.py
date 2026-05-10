import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

# Delete existing admin if present
CustomUser.objects.filter(username='admin').delete()

# Create new superuser
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@school.com',
    password='Admin123!@#'
)
print(f'✅ Superuser created: {admin}')
print(f'✅ Username: admin')
print(f'✅ Email: admin@school.com')
print(f'✅ Password: Admin123!@#')

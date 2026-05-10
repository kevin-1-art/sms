from django.urls import path
from apps.users.dashboard_views import admin_dashboard, teacher_dashboard, student_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),
]

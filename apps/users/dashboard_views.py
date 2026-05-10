from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.academics.models import Class, Subject, Result
from apps.attendance.models import Attendance

@login_required
def admin_dashboard(request):
    """Admin dashboard view."""
    if not request.user.is_admin() and request.user.is_superuser is False:
        return render(request, '404.html', status=403)
    
    context = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'total_classes': Class.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    """Teacher dashboard view."""
    if not request.user.is_teacher():
        return render(request, '404.html', status=403)
    
    try:
        teacher = request.user.teacher_profile
        context = {
            'assigned_classes': teacher.get_assigned_classes(),
            'assigned_subjects': teacher.get_assigned_subjects(),
            'total_students': Student.objects.filter(current_class__in=teacher.classes.all()).count(),
        }
    except:
        context = {
            'assigned_classes': [],
            'assigned_subjects': [],
            'total_students': 0,
        }
    
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    """Student dashboard view."""
    if not request.user.is_student():
        return render(request, '404.html', status=403)
    
    try:
        student = request.user.student_profile
        context = {
            'student': student,
            'current_class': student.current_class,
            'recent_results': student.results.all()[:5],
            'attendance_count': student.attendance_records.filter(status='Present').count(),
        }
    except:
        context = {
            'student': None,
            'current_class': None,
            'recent_results': [],
            'attendance_count': 0,
        }
    
    return render(request, 'dashboard/student_dashboard.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from apps.attendance.models import Attendance, AttendanceSummary
from apps.attendance.forms import AttendanceForm, BulkAttendanceForm
from apps.academics.models import Class
from apps.students.models import Student

@login_required
def attendance_list(request):
    """Display list of attendance records."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_teacher():
            return render(request, '404.html', status=403)
    
    attendance_records = Attendance.objects.select_related('student', 'class_obj', 'subject').all()
    
    # Filter by date
    date_filter = request.GET.get('date', '')
    if date_filter:
        attendance_records = attendance_records.filter(date=date_filter)
    else:
        # Default to today
        today = timezone.now().date()
        attendance_records = attendance_records.filter(date=today)
    
    # Filter by class
    class_filter = request.GET.get('class', '')
    if class_filter:
        attendance_records = attendance_records.filter(class_obj__id=class_filter)
    
    context = {
        'attendance_records': attendance_records,
        'classes': Class.objects.filter(is_active=True),
        'date_filter': date_filter,
        'class_filter': class_filter,
    }
    return render(request, 'attendance/attendance_list.html', context)


@login_required
def mark_attendance(request):
    """Mark attendance for a single student."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_teacher():
            return render(request, '404.html', status=403)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm()
    
    return render(request, 'attendance/mark_attendance.html', {'form': form})


@login_required
def bulk_mark_attendance(request):
    """Mark attendance for all students in a class."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_teacher():
            return render(request, '404.html', status=403)
    
    students = []
    selected_class = None
    
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            selected_class = form.cleaned_data['class_obj']
            subject = form.cleaned_data.get('subject')
            date = form.cleaned_data['date']
            
            # Get all students in the class
            students = Student.objects.filter(current_class=selected_class, is_active=True)
            
            # Mark attendance for each student
            for student in students:
                status = request.POST.get(f'status_{student.id}', 'Present')
                remarks = request.POST.get(f'remarks_{student.id}', '')
                
                # Check if attendance already exists for this date
                attendance, created = Attendance.objects.get_or_create(
                    student=student,
                    date=date,
                    subject=subject,
                    defaults={
                        'class_obj': selected_class,
                        'status': status,
                        'remarks': remarks,
                        'marked_by': request.user
                    }
                )
                
                if not created:
                    attendance.status = status
                    attendance.remarks = remarks
                    attendance.marked_by = request.user
                    attendance.save()
            
            messages.success(request, f'Attendance marked for {len(students)} students.')
            return redirect('attendance:attendance_list')
    else:
        form = BulkAttendanceForm()
        # If class is specified in GET params, fetch students
        class_id = request.GET.get('class_id')
        if class_id:
            try:
                selected_class = Class.objects.get(id=class_id)
                students = Student.objects.filter(current_class=selected_class, is_active=True)
            except Class.DoesNotExist:
                pass
    
    context = {
        'form': form,
        'students': students,
        'selected_class': selected_class,
    }
    return render(request, 'attendance/bulk_mark_attendance.html', context)


@login_required
def attendance_report(request):
    """View attendance reports for students."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_student():
            return render(request, '404.html', status=403)
    
    # If student, show their own attendance
    if request.user.is_student():
        try:
            student = request.user.student_profile
            attendance_records = student.attendance_records.all()
        except:
            attendance_records = []
    else:
        # If admin/teacher, allow filtering
        attendance_records = Attendance.objects.select_related('student').all()
        
        student_filter = request.GET.get('student', '')
        if student_filter:
            attendance_records = attendance_records.filter(student__id=student_filter)
    
    context = {
        'attendance_records': attendance_records,
        'students': Student.objects.filter(is_active=True),
    }
    return render(request, 'attendance/attendance_report.html', context)


@login_required
def student_attendance_report(request, student_id):
    """View detailed attendance report for a specific student."""
    student = get_object_or_404(Student, pk=student_id)
    
    # Check permissions
    if not request.user.is_admin() and not request.user.is_superuser:
        if request.user != student.user:
            return render(request, '404.html', status=403)
    
    # Get current date info
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Get attendance for current month
    attendance_records = student.attendance_records.filter(
        date__month=current_month,
        date__year=current_year
    )
    
    # Calculate statistics
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='Present').count()
    absent_days = attendance_records.filter(status='Absent').count()
    leave_days = attendance_records.filter(status='Leave').count()
    
    percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'leave_days': leave_days,
        'percentage': percentage,
    }
    return render(request, 'attendance/student_attendance_report.html', context)

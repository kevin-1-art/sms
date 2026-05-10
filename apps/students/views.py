from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from apps.students.models import Student
from apps.students.forms import StudentForm

@login_required
def student_list(request):
    """Display list of all students with search and filter functionality."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    students = Student.objects.select_related('user', 'current_class').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(admission_number__icontains=search_query) |
            Q(guardian_name__icontains=search_query)
        )
    
    # Filter by class
    class_filter = request.GET.get('class', '')
    if class_filter:
        students = students.filter(current_class__id=class_filter)
    
    context = {
        'students': students,
        'search_query': search_query,
        'class_filter': class_filter,
    }
    return render(request, 'students/student_list.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def student_create(request):
    """Create a new student record."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record created successfully.')
            return redirect('students:student_list')
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Create Student'})


@login_required
@require_http_methods(["GET", "POST"])
def student_edit(request, pk):
    """Edit student record."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record updated successfully.')
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Edit {student.user.get_full_name()}'
    })


@login_required
def student_detail(request, pk):
    """View student details."""
    student = get_object_or_404(Student, pk=pk)
    
    # Check permissions
    if not request.user.is_admin() and not request.user.is_superuser:
        if request.user != student.user:
            return render(request, '404.html', status=403)
    
    context = {
        'student': student,
        'results': student.results.all(),
        'attendance_records': student.attendance_records.all()[:10],
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def student_delete(request, pk):
    """Delete (deactivate) student record."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, 'Student record has been deactivated.')
        return redirect('students:student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})

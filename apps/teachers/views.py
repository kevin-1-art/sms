from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.teachers.models import Teacher
from apps.teachers.forms import TeacherForm

@login_required
def teacher_list(request):
    """Display list of all teachers."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    teachers = Teacher.objects.select_related('user').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query)
        )
    
    context = {
        'teachers': teachers,
        'search_query': search_query,
    }
    return render(request, 'teachers/teacher_list.html', context)


@login_required
def teacher_create(request):
    """Create a new teacher record."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher record created successfully.')
            return redirect('teachers:teacher_list')
    else:
        form = TeacherForm()
    
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Create Teacher'})


@login_required
def teacher_edit(request, pk):
    """Edit teacher record."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher record updated successfully.')
            return redirect('teachers:teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    
    return render(request, 'teachers/teacher_form.html', {
        'form': form,
        'teacher': teacher,
        'title': f'Edit {teacher.user.get_full_name()}'
    })


@login_required
def teacher_detail(request, pk):
    """View teacher details."""
    teacher = get_object_or_404(Teacher, pk=pk)
    
    # Check permissions
    if not request.user.is_admin() and not request.user.is_superuser:
        if request.user != teacher.user:
            return render(request, '404.html', status=403)
    
    context = {
        'teacher': teacher,
        'assigned_classes': teacher.get_assigned_classes(),
        'assigned_subjects': teacher.get_assigned_subjects(),
    }
    return render(request, 'teachers/teacher_detail.html', context)


@login_required
def teacher_delete(request, pk):
    """Delete (deactivate) teacher record."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        teacher.is_active = False
        teacher.save()
        messages.success(request, 'Teacher record has been deactivated.')
        return redirect('teachers:teacher_list')
    
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})

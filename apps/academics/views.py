from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from apps.academics.models import Class, Subject, SubjectClass, Result
from apps.academics.forms import ClassForm, SubjectForm, SubjectClassForm, ResultForm
from apps.students.models import Student

# ============ CLASS VIEWS ============

@login_required
def class_list(request):
    """Display list of all classes."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    classes = Class.objects.select_related('class_teacher__user').filter(is_active=True)
    
    context = {
        'classes': classes,
    }
    return render(request, 'academics/class_list.html', context)


@login_required
def class_create(request):
    """Create a new class."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully.')
            return redirect('academics:class_list')
    else:
        form = ClassForm()
    
    return render(request, 'academics/class_form.html', {'form': form, 'title': 'Create Class'})


@login_required
def class_edit(request, pk):
    """Edit class details."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    class_obj = get_object_or_404(Class, pk=pk)
    
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully.')
            return redirect('academics:class_list')
    else:
        form = ClassForm(instance=class_obj)
    
    return render(request, 'academics/class_form.html', {
        'form': form,
        'class_obj': class_obj,
        'title': f'Edit {class_obj.name}'
    })


# ============ SUBJECT VIEWS ============

@login_required
def subject_list(request):
    """Display list of all subjects."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    subjects = Subject.objects.filter(is_active=True)
    
    context = {
        'subjects': subjects,
    }
    return render(request, 'academics/subject_list.html', context)


@login_required
def subject_create(request):
    """Create a new subject."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm()
    
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Create Subject'})


@login_required
def subject_edit(request, pk):
    """Edit subject details."""
    if not request.user.is_admin() and not request.user.is_superuser:
        return render(request, '404.html', status=403)
    
    subject = get_object_or_404(Subject, pk=pk)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'academics/subject_form.html', {
        'form': form,
        'subject': subject,
        'title': f'Edit {subject.name}'
    })


# ============ RESULT VIEWS ============

@login_required
def result_list(request):
    """Display list of results."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_teacher():
            return render(request, '404.html', status=403)
    
    results = Result.objects.select_related('student', 'subject').all()
    
    # Filter by student
    student_filter = request.GET.get('student', '')
    if student_filter:
        results = results.filter(student__id=student_filter)
    
    # Filter by term
    term_filter = request.GET.get('term', '')
    if term_filter:
        results = results.filter(term=term_filter)
    
    context = {
        'results': results,
        'students': Student.objects.filter(is_active=True),
    }
    return render(request, 'academics/result_list.html', context)


@login_required
def result_create(request):
    """Create a new result/grade entry."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_teacher():
            return render(request, '404.html', status=403)
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.save()
            messages.success(request, 'Result/Grade recorded successfully.')
            return redirect('academics:result_list')
    else:
        form = ResultForm()
    
    return render(request, 'academics/result_form.html', {'form': form, 'title': 'Enter Result/Grade'})


@login_required
def result_edit(request, pk):
    """Edit result/grade entry."""
    if not request.user.is_admin() and not request.user.is_superuser:
        if not request.user.is_teacher():
            return render(request, '404.html', status=403)
    
    result = get_object_or_404(Result, pk=pk)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result/Grade updated successfully.')
            return redirect('academics:result_list')
    else:
        form = ResultForm(instance=result)
    
    return render(request, 'academics/result_form.html', {
        'form': form,
        'result': result,
        'title': 'Edit Result/Grade'
    })


@login_required
def report_card(request, student_id):
    """Display student's report card."""
    student = get_object_or_404(Student, pk=student_id)
    
    # Check permissions
    if not request.user.is_admin() and not request.user.is_superuser:
        if request.user != student.user:
            return render(request, '404.html', status=403)
    
    # Get results grouped by term
    results_by_term = {}
    for term in ['Term1', 'Term2', 'Final']:
        results_by_term[term] = student.results.filter(term=term)
    
    context = {
        'student': student,
        'results_by_term': results_by_term,
    }
    return render(request, 'academics/report_card.html', context)

from django.contrib import admin
from apps.academics.models import Class, Subject, SubjectClass, Result

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """Admin interface for Class model."""
    list_display = ['name', 'class_level', 'section', 'capacity', 'class_teacher', 'is_active']
    list_filter = ['class_level', 'is_active', 'created_at']
    search_fields = ['name', 'section']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin interface for Subject model."""
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SubjectClass)
class SubjectClassAdmin(admin.ModelAdmin):
    """Admin interface for SubjectClass model."""
    list_display = ['subject', 'class_obj', 'teacher', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['subject__name', 'class_obj__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Admin interface for Result model."""
    list_display = ['student', 'subject', 'marks_obtained', 'grade', 'term', 'academic_year']
    list_filter = ['term', 'academic_year', 'grade', 'created_at']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'subject__name']
    readonly_fields = ['grade', 'created_at', 'updated_at']

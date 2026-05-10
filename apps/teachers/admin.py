from django.contrib import admin
from apps.teachers.models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin interface for Teacher model."""
    list_display = ['user', 'employee_id', 'qualification', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    filter_horizontal = ['subjects', 'classes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('employee_id', 'date_of_joining', 'qualification', 'specialization')
        }),
        ('Assignments', {
            'fields': ('subjects', 'classes')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

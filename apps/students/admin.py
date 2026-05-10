from django.contrib import admin
from apps.students.models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model."""
    list_display = ['user', 'admission_number', 'current_class', 'guardian_name', 'is_active']
    list_filter = ['current_class', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'admission_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Student Information', {
            'fields': ('admission_number', 'gender', 'date_of_birth', 'current_class')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email', 'guardian_address')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

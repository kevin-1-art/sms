from django.contrib import admin
from apps.attendance.models import Attendance, AttendanceSummary

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin interface for Attendance model."""
    list_display = ['student', 'date', 'status', 'class_obj', 'marked_by']
    list_filter = ['status', 'date', 'class_obj']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'date']
    readonly_fields = ['created_at', 'updated_at', 'marked_by']

@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    """Admin interface for AttendanceSummary model."""
    list_display = ['student', 'month', 'year', 'percentage']
    list_filter = ['month', 'year']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    readonly_fields = ['updated_at']

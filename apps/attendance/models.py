from django.db import models
from django.utils import timezone

ATTENDANCE_STATUS_CHOICES = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Leave', 'Leave'),
)

class Attendance(models.Model):
    """Daily attendance record."""
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    class_obj = models.ForeignKey(
        'academics.Class',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    subject = models.ForeignKey(
        'academics.Subject',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='attendance_records'
    )
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=ATTENDANCE_STATUS_CHOICES,
        default='Present'
    )
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_marked'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance_attendance'
        ordering = ['-date', 'student__user__first_name']
        unique_together = ['student', 'date', 'subject']

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"


class AttendanceSummary(models.Model):
    """Summary of attendance per student per month."""
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_summaries'
    )
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    year = models.IntegerField()
    total_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    leave_days = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance_summary'
        ordering = ['-year', '-month']
        unique_together = ['student', 'month', 'year']

    def __str__(self):
        return f"{self.student} - {self.month}/{self.year}"

    def calculate_percentage(self):
        """Calculate attendance percentage."""
        if self.total_days > 0:
            return (self.present_days / self.total_days) * 100
        return 0.0

    def save(self, *args, **kwargs):
        """Auto-calculate percentage before saving."""
        self.percentage = self.calculate_percentage()
        super().save(*args, **kwargs)

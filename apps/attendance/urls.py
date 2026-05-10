from django.urls import path
from apps.attendance.views import (
    attendance_list, mark_attendance, bulk_mark_attendance,
    attendance_report, student_attendance_report
)

app_name = 'attendance'

urlpatterns = [
    path('', attendance_list, name='attendance_list'),
    path('mark/', mark_attendance, name='mark_attendance'),
    path('bulk-mark/', bulk_mark_attendance, name='bulk_mark_attendance'),
    path('report/', attendance_report, name='attendance_report'),
    path('student/<int:student_id>/report/', student_attendance_report, name='student_attendance_report'),
]

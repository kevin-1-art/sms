from django.urls import path
from apps.students.views import (
    student_list, student_create, student_edit,
    student_detail, student_delete
)

app_name = 'students'

urlpatterns = [
    path('', student_list, name='student_list'),
    path('create/', student_create, name='student_create'),
    path('<int:pk>/', student_detail, name='student_detail'),
    path('<int:pk>/edit/', student_edit, name='student_edit'),
    path('<int:pk>/delete/', student_delete, name='student_delete'),
]

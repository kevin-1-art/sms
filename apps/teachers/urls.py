from django.urls import path
from apps.teachers.views import (
    teacher_list, teacher_create, teacher_edit,
    teacher_detail, teacher_delete
)

app_name = 'teachers'

urlpatterns = [
    path('', teacher_list, name='teacher_list'),
    path('create/', teacher_create, name='teacher_create'),
    path('<int:pk>/', teacher_detail, name='teacher_detail'),
    path('<int:pk>/edit/', teacher_edit, name='teacher_edit'),
    path('<int:pk>/delete/', teacher_delete, name='teacher_delete'),
]

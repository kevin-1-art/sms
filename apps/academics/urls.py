from django.urls import path
from apps.academics.views import (
    class_list, class_create, class_edit,
    subject_list, subject_create, subject_edit,
    result_list, result_create, result_edit,
    report_card
)

app_name = 'academics'

urlpatterns = [
    # Class URLs
    path('classes/', class_list, name='class_list'),
    path('classes/create/', class_create, name='class_create'),
    path('classes/<int:pk>/edit/', class_edit, name='class_edit'),
    
    # Subject URLs
    path('subjects/', subject_list, name='subject_list'),
    path('subjects/create/', subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', subject_edit, name='subject_edit'),
    
    # Result URLs
    path('results/', result_list, name='result_list'),
    path('results/create/', result_create, name='result_create'),
    path('results/<int:pk>/edit/', result_edit, name='result_edit'),
    
    # Report Card
    path('report-card/<int:student_id>/', report_card, name='report_card'),
]

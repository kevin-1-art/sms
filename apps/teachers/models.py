from django.db import models
from apps.users.models import CustomUser

class Teacher(models.Model):
    """Teacher model with employment information."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    employee_id = models.CharField(max_length=50, unique=True)
    date_of_joining = models.DateField()
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    
    # Subjects and classes assignment
    subjects = models.ManyToManyField(
        'academics.Subject',
        related_name='teachers'
    )
    classes = models.ManyToManyField(
        'academics.Class',
        related_name='teachers'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teachers_teacher'
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    def get_assigned_classes(self):
        """Get all classes assigned to this teacher."""
        return self.classes.all()

    def get_assigned_subjects(self):
        """Get all subjects assigned to this teacher."""
        return self.subjects.all()

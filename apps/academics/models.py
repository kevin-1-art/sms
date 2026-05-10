from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

GRADE_CHOICES = (
    ('A', 'A - Excellent'),
    ('B', 'B - Good'),
    ('C', 'C - Average'),
    ('D', 'D - Below Average'),
    ('F', 'F - Fail'),
)

class Class(models.Model):
    """Class/Grade model."""
    name = models.CharField(max_length=100, unique=True)  # e.g., "Class 10-A"
    class_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    section = models.CharField(max_length=10)  # e.g., "A", "B", "C"
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    class_teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_classes'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academics_class'
        ordering = ['class_level', 'section']
        unique_together = ['class_level', 'section']

    def __str__(self):
        return f"{self.name}"

    def get_student_count(self):
        """Get current student count in the class."""
        return self.students.filter(is_active=True).count()


class Subject(models.Model):
    """Subject model."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academics_subject'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class SubjectClass(models.Model):
    """Link between subjects and classes."""
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_assignments'
    )
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='subject_assignments'
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subject_classes'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academics_subject_class'
        unique_together = ['subject', 'class_obj']
        ordering = ['subject__name']

    def __str__(self):
        return f"{self.subject.name} - {self.class_obj.name}"


class Result(models.Model):
    """Student results/grades model."""
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='results'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='results'
    )
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='results'
    )
    marks_obtained = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    term = models.CharField(
        max_length=20,
        choices=[('Term1', 'Term 1'), ('Term2', 'Term 2'), ('Final', 'Final')]
    )
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_results'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academics_result'
        ordering = ['-academic_year', 'term', 'subject__name']
        unique_together = ['student', 'subject', 'class_obj', 'term', 'academic_year']

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks_obtained} ({self.grade})"

    def calculate_grade(self):
        """Calculate grade based on marks obtained."""
        marks = self.marks_obtained
        if marks >= 80:
            return 'A'
        elif marks >= 70:
            return 'B'
        elif marks >= 60:
            return 'C'
        elif marks >= 50:
            return 'D'
        else:
            return 'F'

    def save(self, *args, **kwargs):
        """Auto-calculate grade before saving."""
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

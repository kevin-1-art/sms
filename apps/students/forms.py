from django import forms
from apps.students.models import Student

class StudentForm(forms.ModelForm):
    """Form for creating/updating student records."""
    class Meta:
        model = Student
        fields = [
            'admission_number', 'gender', 'date_of_birth',
            'guardian_name', 'guardian_phone', 'guardian_email',
            'guardian_address', 'current_class'
        ]
        widgets = {
            'admission_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'guardian_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'current_class': forms.Select(attrs={'class': 'form-control'}),
        }

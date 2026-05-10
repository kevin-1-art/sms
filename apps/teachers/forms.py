from django import forms
from apps.teachers.models import Teacher

class TeacherForm(forms.ModelForm):
    """Form for creating/updating teacher records."""
    class Meta:
        model = Teacher
        fields = [
            'employee_id', 'date_of_joining', 'qualification',
            'specialization', 'subjects', 'classes'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'subjects': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'classes': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

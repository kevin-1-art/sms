from django import forms
from apps.academics.models import Class, Subject, SubjectClass, Result

class ClassForm(forms.ModelForm):
    """Form for creating/updating class."""
    class Meta:
        model = Class
        fields = ['name', 'class_level', 'section', 'capacity', 'class_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    """Form for creating/updating subject."""
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class SubjectClassForm(forms.ModelForm):
    """Form for assigning subjects to classes."""
    class Meta:
        model = SubjectClass
        fields = ['subject', 'class_obj', 'teacher']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'class_obj': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class ResultForm(forms.ModelForm):
    """Form for entering student results."""
    class Meta:
        model = Result
        fields = ['student', 'subject', 'class_obj', 'marks_obtained', 'term', 'academic_year', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'class_obj': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.5
            }),
            'term': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2023-2024'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

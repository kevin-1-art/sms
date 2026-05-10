from django import forms
from django.forms import inlineformset_factory
from apps.attendance.models import Attendance, AttendanceSummary

class AttendanceForm(forms.ModelForm):
    """Form for marking attendance."""
    class Meta:
        model = Attendance
        fields = ['student', 'class_obj', 'subject', 'date', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'class_obj': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }

class BulkAttendanceForm(forms.Form):
    """Form for bulk marking attendance."""
    class_obj = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Class'
    )
    subject = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Subject (Optional)'
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        from apps.academics.models import Class, Subject
        super().__init__(*args, **kwargs)
        self.fields['class_obj'].queryset = Class.objects.filter(is_active=True)
        self.fields['subject'].queryset = Subject.objects.filter(is_active=True)

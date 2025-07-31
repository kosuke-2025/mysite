from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['in_out']
        widgets = {
            'in_out': forms.RadioSelect,
        }
        labels = {
            'in_out': '現在のステータス',
        }
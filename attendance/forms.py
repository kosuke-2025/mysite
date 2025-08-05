from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['in_out', 'comment']
        widgets = {
            'in_out': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': '今日の独り言…'}),
        }
        labels = {
            'in_out': '現在のステータス',
            'comment': 'コメント',
        }
from django import forms

from .models import Attendance


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ("child", "date", "status", "arrival_time", "departure_time", "note")
        widgets = {
            "child": forms.Select(attrs={"class": "input"}),
            "date": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "status": forms.Select(attrs={"class": "input"}),
            "arrival_time": forms.TimeInput(attrs={"class": "input", "type": "time"}),
            "departure_time": forms.TimeInput(attrs={"class": "input", "type": "time"}),
            "note": forms.Textarea(attrs={"class": "input", "rows": 2}),
        }

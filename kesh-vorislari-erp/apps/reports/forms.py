from django import forms

from .models import DailyReport


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = (
            "child",
            "date",
            "mood",
            "breakfast_status",
            "lunch_status",
            "snack_status",
            "nap_duration",
            "activity_participation",
            "note",
        )
        widgets = {
            "child": forms.Select(attrs={"class": "input"}),
            "date": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "mood": forms.Select(attrs={"class": "input"}),
            "breakfast_status": forms.Select(attrs={"class": "input"}),
            "lunch_status": forms.Select(attrs={"class": "input"}),
            "snack_status": forms.Select(attrs={"class": "input"}),
            "nap_duration": forms.TextInput(attrs={"class": "input", "placeholder": "01:30:00"}),
            "activity_participation": forms.Select(attrs={"class": "input"}),
            "note": forms.Textarea(attrs={"class": "input", "rows": 3}),
        }

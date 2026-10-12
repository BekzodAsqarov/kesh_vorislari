from django import forms

from apps.accounts.models import User
from apps.groups.models import Group

from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            "title",
            "description",
            "activity_type",
            "group",
            "teacher",
            "date",
            "start_time",
            "end_time",
            "location",
            "notes",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "input", "rows": 3}),
            "activity_type": forms.Select(attrs={"class": "input"}),
            "group": forms.Select(attrs={"class": "input"}),
            "teacher": forms.Select(attrs={"class": "input"}),
            "date": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "input", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "input", "type": "time"}),
            "location": forms.TextInput(attrs={"class": "input"}),
            "notes": forms.Textarea(attrs={"class": "input", "rows": 2}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and not user.is_admin:
            from apps.groups.selectors import groups_for_user

            self.fields["group"].queryset = groups_for_user(user)
            self.fields["teacher"].queryset = User.objects.filter(pk=user.pk)
            self.fields["teacher"].initial = user
        else:
            self.fields["teacher"].queryset = User.objects.filter(role=User.Role.TEACHER)
            self.fields["group"].queryset = Group.objects.filter(is_active=True)

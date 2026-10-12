from django import forms

from apps.accounts.models import User

from .models import Group


class GroupForm(forms.ModelForm):
    teachers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.TEACHER, is_active=True),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "input"}),
    )

    class Meta:
        model = Group
        fields = ("name", "description", "room", "age_min", "age_max", "teachers", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "input", "rows": 3}),
            "room": forms.TextInput(attrs={"class": "input"}),
            "age_min": forms.NumberInput(attrs={"class": "input"}),
            "age_max": forms.NumberInput(attrs={"class": "input"}),
        }

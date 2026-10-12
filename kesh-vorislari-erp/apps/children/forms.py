from django import forms

from apps.accounts.models import User
from apps.groups.models import Group

from .models import Child


class ChildForm(forms.ModelForm):
    parents = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.PARENT, is_active=True),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "input"}),
    )

    class Meta:
        model = Child
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "group",
            "parents",
            "contact_phone",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "allergies",
            "medical_notes",
            "enrollment_date",
            "is_active",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "date_of_birth": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "gender": forms.Select(attrs={"class": "input"}),
            "group": forms.Select(attrs={"class": "input"}),
            "contact_phone": forms.TextInput(attrs={"class": "input"}),
            "address": forms.TextInput(attrs={"class": "input"}),
            "emergency_contact_name": forms.TextInput(attrs={"class": "input"}),
            "emergency_contact_phone": forms.TextInput(attrs={"class": "input"}),
            "allergies": forms.Textarea(attrs={"class": "input", "rows": 2}),
            "medical_notes": forms.Textarea(attrs={"class": "input", "rows": 2}),
            "enrollment_date": forms.DateInput(attrs={"class": "input", "type": "date"}),
        }

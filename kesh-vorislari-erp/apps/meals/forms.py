from django import forms
from django.forms import inlineformset_factory

from .models import Meal, Menu, MenuItem


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ("name", "category", "description", "ingredients", "allergens", "portion", "notes", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "input"}),
            "category": forms.Select(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "input", "rows": 2}),
            "ingredients": forms.Textarea(attrs={"class": "input", "rows": 2}),
            "allergens": forms.TextInput(attrs={"class": "input"}),
            "portion": forms.TextInput(attrs={"class": "input"}),
            "notes": forms.Textarea(attrs={"class": "input", "rows": 2}),
        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ("date", "notes")
        widgets = {
            "date": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "input", "rows": 2}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ("meal", "category", "name", "allergens", "portion", "sort_order")
        widgets = {
            "meal": forms.Select(attrs={"class": "input"}),
            "category": forms.Select(attrs={"class": "input"}),
            "name": forms.TextInput(attrs={"class": "input"}),
            "allergens": forms.TextInput(attrs={"class": "input"}),
            "portion": forms.TextInput(attrs={"class": "input"}),
            "sort_order": forms.NumberInput(attrs={"class": "input"}),
        }


MenuItemFormSet = inlineformset_factory(
    Menu,
    MenuItem,
    form=MenuItemForm,
    extra=4,
    can_delete=True,
)

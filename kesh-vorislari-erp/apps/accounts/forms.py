from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "input", "autofocus": True, "placeholder": "you@example.com"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Password"}),
    )


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "input"}))

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "phone", "is_active")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "input"}),
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "role": forms.Select(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        elif not user.pk:
            raise forms.ValidationError("Password is required for new users.")
        if commit:
            user.save()
        return user

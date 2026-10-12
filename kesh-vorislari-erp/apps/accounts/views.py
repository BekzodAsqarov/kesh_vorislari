from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.decorators import role_required

from .forms import EmailAuthenticationForm, UserForm
from .models import User
from .selectors import users_visible_to
from .services import ensure_role_profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f"Welcome back, {request.user.get_short_name()}.")
        return redirect("dashboard:index")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"profile_user": request.user})


@role_required()
def user_list(request):
    return render(request, "accounts/user_list.html", {"users": users_visible_to(request.user)})


@role_required()
def user_create(request):
    form = UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        ensure_role_profile(user)
        messages.success(request, "User created.")
        return redirect("accounts:users")
    return render(request, "accounts/user_form.html", {"form": form, "title": "Create user"})


@role_required()
def user_update(request, pk: int):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        ensure_role_profile(user)
        messages.success(request, "User updated.")
        return redirect("accounts:users")
    return render(request, "accounts/user_form.html", {"form": form, "title": "Edit user"})

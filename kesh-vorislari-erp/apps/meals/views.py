from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.core.decorators import role_required

from .forms import MealForm, MenuForm, MenuItemFormSet
from .models import Meal, Menu


@login_required
def menu_list(request):
    today = timezone.localdate()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    menus = Menu.objects.filter(date__range=(start, end)).prefetch_related("items").order_by("date")
    catalog = Meal.objects.filter(is_active=True)
    return render(
        request,
        "meals/list.html",
        {"menus": menus, "start": start, "end": end, "catalog": catalog, "today": today},
    )


@login_required
def menu_detail(request, pk: int):
    menu = get_object_or_404(Menu.objects.prefetch_related("items"), pk=pk)
    return render(request, "meals/detail.html", {"menu": menu})


@role_required()
def menu_create(request):
    form = MenuForm(request.POST or None)
    formset = MenuItemFormSet(request.POST or None)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        menu = form.save(commit=False)
        menu.created_by = request.user
        menu.save()
        formset.instance = menu
        formset.save()
        messages.success(request, "Menu saved.")
        return redirect("meals:detail", pk=menu.pk)
    return render(request, "meals/form.html", {"form": form, "formset": formset, "title": "Create menu"})


@role_required()
def menu_update(request, pk: int):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(request.POST or None, instance=menu)
    formset = MenuItemFormSet(request.POST or None, instance=menu)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, "Menu updated.")
        return redirect("meals:detail", pk=menu.pk)
    return render(request, "meals/form.html", {"form": form, "formset": formset, "title": "Edit menu"})


@role_required()
def meal_create(request):
    form = MealForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Meal added to catalog.")
        return redirect("meals:list")
    return render(request, "meals/meal_form.html", {"form": form, "title": "Add meal"})

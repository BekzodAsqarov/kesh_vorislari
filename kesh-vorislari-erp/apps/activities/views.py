from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.core.decorators import role_required

from .forms import ActivityForm
from .selectors import activities_for_user


@login_required
def activity_list(request):
    qs = activities_for_user(request.user)
    selected_date = request.GET.get("date")
    if selected_date:
        qs = qs.filter(date=selected_date)
    return render(
        request,
        "activities/list.html",
        {"activities": qs, "selected_date": selected_date or timezone.localdate().isoformat()},
    )


@login_required
def activity_detail(request, pk: int):
    activity = get_object_or_404(activities_for_user(request.user), pk=pk)
    return render(request, "activities/detail.html", {"activity": activity})


@role_required("TEACHER")
def activity_create(request):
    form = ActivityForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Activity created.")
        return redirect("activities:list")
    return render(request, "activities/form.html", {"form": form, "title": "Create activity"})


@role_required("TEACHER")
def activity_update(request, pk: int):
    activity = get_object_or_404(activities_for_user(request.user), pk=pk)
    form = ActivityForm(request.POST or None, instance=activity, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Activity updated.")
        return redirect("activities:detail", pk=activity.pk)
    return render(request, "activities/form.html", {"form": form, "title": "Edit activity"})

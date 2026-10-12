from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.decorators import role_required

from .forms import GroupForm
from .models import Group
from .selectors import groups_for_user


@login_required
def group_list(request):
    return render(request, "groups/list.html", {"groups": groups_for_user(request.user)})


@login_required
def group_detail(request, pk: int):
    group = get_object_or_404(groups_for_user(request.user), pk=pk)
    return render(request, "groups/detail.html", {"group": group})


@role_required()
def group_create(request):
    form = GroupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Group created.")
        return redirect("groups:list")
    return render(request, "groups/form.html", {"form": form, "title": "Create group"})


@role_required()
def group_update(request, pk: int):
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(request.POST or None, instance=group)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Group updated.")
        return redirect("groups:detail", pk=group.pk)
    return render(request, "groups/form.html", {"form": form, "title": "Edit group"})

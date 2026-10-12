from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.decorators import role_required
from apps.groups.selectors import groups_for_user

from .forms import ChildForm
from .models import Child
from .selectors import children_for_user


@login_required
def child_list(request):
    qs = children_for_user(request.user)
    q = request.GET.get("q", "").strip()
    group_id = request.GET.get("group")
    if q:
        qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    if group_id:
        qs = qs.filter(group_id=group_id)
    return render(
        request,
        "children/list.html",
        {"children": qs, "q": q, "groups": groups_for_user(request.user), "selected_group": group_id},
    )


@login_required
def child_detail(request, pk: int):
    child = get_object_or_404(children_for_user(request.user), pk=pk)
    return render(request, "children/detail.html", {"child": child})


@role_required()
def child_create(request):
    form = ChildForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Child profile created.")
        return redirect("children:list")
    return render(request, "children/form.html", {"form": form, "title": "Add child"})


@role_required()
def child_update(request, pk: int):
    child = get_object_or_404(Child, pk=pk)
    form = ChildForm(request.POST or None, instance=child)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Child profile updated.")
        return redirect("children:detail", pk=child.pk)
    return render(request, "children/form.html", {"form": form, "title": "Edit child"})

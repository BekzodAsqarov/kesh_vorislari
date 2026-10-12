from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.children.models import Child
from apps.children.selectors import children_for_user
from apps.core.decorators import role_required
from apps.core.exceptions import DomainError
from apps.groups.selectors import groups_for_user

from .forms import AttendanceForm
from .models import Attendance
from .selectors import attendance_for_user
from .services import bulk_record_attendance, record_attendance


@login_required
def attendance_list(request):
    selected_date = request.GET.get("date") or timezone.localdate().isoformat()
    group_id = request.GET.get("group")
    records = attendance_for_user(request.user).filter(date=selected_date)
    if group_id:
        records = records.filter(child__group_id=group_id)
    return render(
        request,
        "attendance/list.html",
        {
            "records": records,
            "selected_date": selected_date,
            "groups": groups_for_user(request.user),
            "selected_group": group_id,
        },
    )


@role_required("TEACHER")
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    form.fields["child"].queryset = children_for_user(request.user)
    if request.method == "POST" and form.is_valid():
        try:
            record_attendance(
                child=form.cleaned_data["child"],
                date_value=form.cleaned_data["date"],
                status=form.cleaned_data["status"],
                recorded_by=request.user,
                arrival_time=form.cleaned_data.get("arrival_time"),
                departure_time=form.cleaned_data.get("departure_time"),
                note=form.cleaned_data.get("note", ""),
            )
            messages.success(request, "Attendance saved.")
            return redirect("attendance:list")
        except DomainError as exc:
            form.add_error(None, str(exc))
    return render(request, "attendance/form.html", {"form": form, "title": "Record attendance"})


@role_required("TEACHER")
def attendance_update(request, pk: int):
    record = get_object_or_404(attendance_for_user(request.user), pk=pk)
    form = AttendanceForm(request.POST or None, instance=record)
    form.fields["child"].queryset = children_for_user(request.user)
    if request.method == "POST" and form.is_valid():
        try:
            record_attendance(
                child=form.cleaned_data["child"],
                date_value=form.cleaned_data["date"],
                status=form.cleaned_data["status"],
                recorded_by=request.user,
                arrival_time=form.cleaned_data.get("arrival_time"),
                departure_time=form.cleaned_data.get("departure_time"),
                note=form.cleaned_data.get("note", ""),
            )
            messages.success(request, "Attendance updated.")
            return redirect("attendance:list")
        except DomainError as exc:
            form.add_error(None, str(exc))
    return render(request, "attendance/form.html", {"form": form, "title": "Edit attendance"})


@role_required("TEACHER")
def attendance_bulk(request):
    groups = groups_for_user(request.user)
    selected_date = request.GET.get("date") or timezone.localdate().isoformat()
    group_id = request.GET.get("group") or (str(groups.first().pk) if groups.exists() else "")
    children = Child.objects.none()
    rows = []
    if group_id:
        children = children_for_user(request.user).filter(group_id=group_id, is_active=True)
        existing = {
            row.child_id: row
            for row in Attendance.objects.filter(date=selected_date, child__in=children)
        }
        rows = [{"child": child, "record": existing.get(child.pk)} for child in children]
    if request.method == "POST":
        group_id = request.POST.get("group")
        selected_date = request.POST.get("date")
        group = get_object_or_404(groups, pk=group_id)
        children = children_for_user(request.user).filter(group=group, is_active=True)
        records = []
        for child in children:
            status = request.POST.get(f"status_{child.pk}")
            if not status:
                continue
            records.append(
                {
                    "child": child,
                    "status": status,
                    "note": request.POST.get(f"note_{child.pk}", ""),
                }
            )
        try:
            bulk_record_attendance(
                group=group,
                date_value=selected_date,
                records=records,
                recorded_by=request.user,
            )
            messages.success(request, "Group attendance saved.")
            return redirect(f"{request.path}?date={selected_date}&group={group.pk}")
        except DomainError as exc:
            messages.error(request, str(exc))
    return render(
        request,
        "attendance/bulk.html",
        {
            "groups": groups,
            "selected_date": selected_date,
            "selected_group": group_id,
            "children": children,
            "rows": rows,
            "statuses": Attendance.Status.choices,
        },
    )

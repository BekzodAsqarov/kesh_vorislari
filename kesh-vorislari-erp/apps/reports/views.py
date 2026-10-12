from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.children.selectors import children_for_user
from apps.core.decorators import role_required
from apps.core.exceptions import DomainError

from .forms import DailyReportForm
from .selectors import reports_for_user
from .services import upsert_daily_report


@login_required
def report_list(request):
    qs = reports_for_user(request.user)
    date_value = request.GET.get("date")
    if date_value:
        qs = qs.filter(date=date_value)
    return render(request, "reports/list.html", {"reports": qs, "selected_date": date_value})


@login_required
def report_detail(request, pk: int):
    report = get_object_or_404(reports_for_user(request.user), pk=pk)
    return render(request, "reports/detail.html", {"report": report})


@role_required("TEACHER")
def report_create(request):
    form = DailyReportForm(request.POST or None)
    form.fields["child"].queryset = children_for_user(request.user)
    if request.method == "POST" and form.is_valid():
        try:
            upsert_daily_report(created_by=request.user, date_value=form.cleaned_data.pop("date"), **form.cleaned_data)
            messages.success(request, "Daily report saved.")
            return redirect("reports:list")
        except DomainError as exc:
            form.add_error(None, str(exc))
    return render(request, "reports/form.html", {"form": form, "title": "New daily report"})


@role_required("TEACHER")
def report_update(request, pk: int):
    report = get_object_or_404(reports_for_user(request.user), pk=pk)
    form = DailyReportForm(request.POST or None, instance=report)
    form.fields["child"].queryset = children_for_user(request.user)
    if request.method == "POST" and form.is_valid():
        try:
            upsert_daily_report(created_by=request.user, date_value=form.cleaned_data.pop("date"), **form.cleaned_data)
            messages.success(request, "Daily report updated.")
            return redirect("reports:detail", pk=report.pk)
        except DomainError as exc:
            form.add_error(None, str(exc))
    return render(request, "reports/form.html", {"form": form, "title": "Edit daily report"})

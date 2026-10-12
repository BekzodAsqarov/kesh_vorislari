from datetime import date

from django.db.models import Count, Q
from django.utils import timezone

from apps.accounts.models import User
from apps.activities.models import Activity
from apps.activities.selectors import activities_for_user
from apps.attendance.models import Attendance
from apps.attendance.selectors import attendance_for_user
from apps.children.models import Child
from apps.children.selectors import children_for_user
from apps.groups.models import Group
from apps.groups.selectors import groups_for_user
from apps.meals.models import Menu
from apps.reports.models import DailyReport


def dashboard_payload(user: User, today: date | None = None) -> dict:
    today = today or timezone.localdate()
    children_qs = children_for_user(user).filter(is_active=True)
    groups_qs = groups_for_user(user).filter(is_active=True)
    attendance_today = attendance_for_user(user).filter(date=today)
    counts = attendance_today.aggregate(
        present=Count("id", filter=Q(status=Attendance.Status.PRESENT)),
        absent=Count("id", filter=Q(status=Attendance.Status.ABSENT)),
        late=Count("id", filter=Q(status=Attendance.Status.LATE)),
        excused=Count("id", filter=Q(status=Attendance.Status.EXCUSED)),
        total=Count("id"),
    )
    activities = activities_for_user(user).filter(date=today)
    menu = Menu.objects.filter(date=today).prefetch_related("items").first()
    recent_reports = (
        DailyReport.objects.select_related("child")
        .filter(child__in=children_qs)
        .order_by("-updated_at")[:8]
    )
    teacher_count = User.objects.filter(role=User.Role.TEACHER, is_active=True).count() if user.is_admin else groups_qs.values("teachers").distinct().count()
    return {
        "today": today,
        "children_count": children_qs.count(),
        "groups_count": groups_qs.count(),
        "teachers_count": teacher_count,
        "attendance": counts,
        "activities": activities,
        "menu": menu,
        "recent_reports": recent_reports,
        "total_children_all": Child.objects.filter(is_active=True).count() if user.is_admin else children_qs.count(),
        "total_groups_all": Group.objects.filter(is_active=True).count() if user.is_admin else groups_qs.count(),
    }

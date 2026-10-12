from django.db.models import QuerySet

from apps.accounts.models import User
from apps.children.selectors import children_for_user

from .models import Attendance


def attendance_for_user(user: User) -> QuerySet[Attendance]:
    return (
        Attendance.objects.select_related("child", "child__group", "recorded_by")
        .filter(child__in=children_for_user(user))
    )

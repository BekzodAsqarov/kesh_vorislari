from django.db.models import QuerySet

from apps.accounts.models import User
from apps.children.selectors import children_for_user

from .models import DailyReport


def reports_for_user(user: User) -> QuerySet[DailyReport]:
    return (
        DailyReport.objects.select_related("child", "child__group", "created_by")
        .filter(child__in=children_for_user(user))
    )

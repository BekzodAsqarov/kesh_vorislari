from datetime import date, timedelta

from apps.accounts.models import User
from apps.children.models import Child
from apps.children.selectors import user_can_access_child
from apps.core.exceptions import DomainError

from .models import DailyReport


def upsert_daily_report(
    *,
    child: Child,
    date_value: date,
    created_by: User,
    mood: str,
    breakfast_status: str,
    lunch_status: str,
    snack_status: str,
    activity_participation: str,
    nap_duration: timedelta | None = None,
    note: str = "",
) -> DailyReport:
    if created_by.is_parent:
        raise DomainError("Parents cannot create or update daily reports.")
    if not created_by.is_admin and not user_can_access_child(created_by, child):
        raise DomainError("You cannot write a report for this child.")
    report, _created = DailyReport.objects.update_or_create(
        child=child,
        date=date_value,
        defaults={
            "mood": mood,
            "breakfast_status": breakfast_status,
            "lunch_status": lunch_status,
            "snack_status": snack_status,
            "nap_duration": nap_duration,
            "activity_participation": activity_participation,
            "note": note,
            "created_by": created_by,
        },
    )
    return report

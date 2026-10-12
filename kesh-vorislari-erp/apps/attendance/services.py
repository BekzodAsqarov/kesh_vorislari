from datetime import date

from django.db import transaction

from apps.accounts.models import User
from apps.children.models import Child
from apps.children.selectors import user_can_access_child
from apps.core.exceptions import DomainError
from apps.groups.models import Group

from .models import Attendance


def record_attendance(
    *,
    child: Child,
    date_value: date,
    status: str,
    recorded_by: User,
    arrival_time=None,
    departure_time=None,
    note: str = "",
) -> Attendance:
    if not user_can_access_child(recorded_by, child) and not recorded_by.is_admin:
        raise DomainError("You cannot record attendance for this child.")
    if arrival_time and departure_time and arrival_time > departure_time:
        raise DomainError("Arrival time must be before departure time.")
    attendance, _created = Attendance.objects.update_or_create(
        child=child,
        date=date_value,
        defaults={
            "status": status,
            "arrival_time": arrival_time,
            "departure_time": departure_time,
            "note": note,
            "recorded_by": recorded_by,
        },
    )
    return attendance


@transaction.atomic
def bulk_record_attendance(*, group: Group, date_value: date, records: list[dict], recorded_by: User) -> list[Attendance]:
    if recorded_by.is_teacher and not group.teachers.filter(pk=recorded_by.pk).exists():
        raise DomainError("You can only record attendance for assigned groups.")
    results = []
    for item in records:
        child = item["child"]
        if child.group_id != group.id:
            raise DomainError(f"{child} is not in group {group.name}.")
        results.append(
            record_attendance(
                child=child,
                date_value=date_value,
                status=item["status"],
                recorded_by=recorded_by,
                arrival_time=item.get("arrival_time"),
                departure_time=item.get("departure_time"),
                note=item.get("note", ""),
            )
        )
    return results

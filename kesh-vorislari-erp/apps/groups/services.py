from django.db import transaction

from apps.accounts.models import User

from .models import Group


@transaction.atomic
def create_group(*, name: str, age_min: int, age_max: int, description: str = "", room: str = "", is_active: bool = True, teachers: list[User] | None = None) -> Group:
    group = Group.objects.create(
        name=name,
        description=description,
        room=room,
        age_min=age_min,
        age_max=age_max,
        is_active=is_active,
    )
    if teachers:
        group.teachers.set(teachers)
    return group

from django.db import transaction

from apps.accounts.models import User
from apps.groups.models import Group

from .models import Child


@transaction.atomic
def create_child(*, first_name: str, last_name: str, date_of_birth, gender: str, group: Group, enrollment_date, parents: list[User] | None = None, **extra) -> Child:
    child = Child.objects.create(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        group=group,
        enrollment_date=enrollment_date,
        **extra,
    )
    if parents:
        child.parents.set(parents)
    return child

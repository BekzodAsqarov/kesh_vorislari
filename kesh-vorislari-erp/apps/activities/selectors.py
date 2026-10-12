from django.db.models import QuerySet

from apps.accounts.models import User
from apps.groups.selectors import groups_for_user

from .models import Activity


def activities_for_user(user: User) -> QuerySet[Activity]:
    qs = Activity.objects.select_related("group", "teacher")
    if user.is_admin:
        return qs
    return qs.filter(group__in=groups_for_user(user))

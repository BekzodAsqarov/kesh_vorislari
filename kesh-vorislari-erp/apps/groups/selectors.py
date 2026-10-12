from django.db.models import QuerySet

from apps.accounts.models import User

from .models import Group


def groups_for_user(user: User) -> QuerySet[Group]:
    qs = Group.objects.all().prefetch_related("teachers")
    if user.is_admin:
        return qs
    if user.is_teacher:
        return qs.filter(teachers=user)
    if user.is_parent:
        return qs.filter(children__parents=user).distinct()
    return qs.none()

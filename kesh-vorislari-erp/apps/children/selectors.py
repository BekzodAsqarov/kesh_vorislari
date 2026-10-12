from django.db.models import QuerySet

from apps.accounts.models import User

from .models import Child


def children_for_user(user: User) -> QuerySet[Child]:
    qs = Child.objects.select_related("group").prefetch_related("parents")
    if user.is_admin:
        return qs
    if user.is_teacher:
        return qs.filter(group__teachers=user)
    if user.is_parent:
        return qs.filter(parents=user)
    return qs.none()


def user_can_access_child(user: User, child: Child) -> bool:
    if user.is_admin:
        return True
    if user.is_teacher:
        return child.group.teachers.filter(pk=user.pk).exists()
    if user.is_parent:
        return child.parents.filter(pk=user.pk).exists()
    return False

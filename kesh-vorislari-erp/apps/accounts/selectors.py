from django.db.models import QuerySet

from .models import User


def teachers() -> QuerySet[User]:
    return User.objects.filter(role=User.Role.TEACHER, is_active=True)


def parents() -> QuerySet[User]:
    return User.objects.filter(role=User.Role.PARENT, is_active=True)


def users_visible_to(user: User) -> QuerySet[User]:
    if user.is_admin:
        return User.objects.all()
    return User.objects.filter(pk=user.pk)

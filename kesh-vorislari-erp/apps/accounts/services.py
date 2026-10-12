from django.db import transaction

from .models import ParentProfile, TeacherProfile, User


@transaction.atomic
def create_user(*, email: str, password: str, first_name: str, last_name: str, role: str, phone: str = "", **profile_fields) -> User:
    """Create a user and the matching profile for teacher/parent roles."""
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role,
        phone=phone,
        is_staff=(role == User.Role.ADMIN),
        is_superuser=(role == User.Role.ADMIN),
    )
    ensure_role_profile(user, **profile_fields)
    return user


def ensure_role_profile(user: User, **profile_fields) -> None:
    if user.role == User.Role.TEACHER:
        TeacherProfile.objects.get_or_create(user=user, defaults=profile_fields)
    elif user.role == User.Role.PARENT:
        ParentProfile.objects.get_or_create(user=user, defaults=profile_fields)


def update_user(user: User, **fields) -> User:
    password = fields.pop("password", None)
    for key, value in fields.items():
        setattr(user, key, value)
    if password:
        user.set_password(password)
    user.save()
    ensure_role_profile(user)
    return user

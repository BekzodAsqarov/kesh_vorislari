from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom user with an explicit role field.

    New roles (COOK, NURSE, ACCOUNTANT, STAFF) can be added to Role
    without changing authentication or JWT. Permissions should check
    `user.role` / helper properties rather than hardcoded user types.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        TEACHER = "TEACHER", "Teacher"
        PARENT = "PARENT", "Parent"
        COOK = "COOK", "Cook"
        NURSE = "NURSE", "Nurse"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        STAFF = "STAFF", "Staff"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=32, choices=Role.choices, db_index=True)
    phone = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["role", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name

    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self) -> bool:
        return self.role == self.Role.TEACHER

    @property
    def is_parent(self) -> bool:
        return self.role == self.Role.PARENT

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)


class TeacherProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    qualification = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Teacher: {self.user.get_full_name()}"


class ParentProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="parent_profile")
    relationship = models.CharField(max_length=64, blank=True, help_text="Mother, father, guardian, …")
    secondary_phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"Parent: {self.user.get_full_name()}"

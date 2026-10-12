from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.groups.models import Group


class Child(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=16, choices=Gender.choices)
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name="children",
    )
    parents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="children",
        blank=True,
        limit_choices_to={"role": "PARENT"},
    )
    contact_phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=255, blank=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=32, blank=True)
    allergies = models.TextField(blank=True)
    medical_notes = models.TextField(blank=True)
    enrollment_date = models.DateField()
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural = "children"
        indexes = [
            models.Index(fields=["group", "is_active"]),
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

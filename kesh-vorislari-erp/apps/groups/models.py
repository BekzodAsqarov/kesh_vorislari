from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Group(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    room = models.CharField(max_length=64, blank=True)
    age_min = models.PositiveSmallIntegerField()
    age_max = models.PositiveSmallIntegerField()
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teaching_groups",
        blank=True,
        limit_choices_to={"role": "TEACHER"},
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(age_min__lte=models.F("age_max")),
                name="group_age_min_lte_age_max",
            ),
        ]

    def __str__(self) -> str:
        return self.name

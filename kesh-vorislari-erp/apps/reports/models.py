from django.conf import settings
from django.db import models

from apps.children.models import Child
from apps.core.models import TimeStampedModel


class DailyReport(TimeStampedModel):
    class Mood(models.TextChoices):
        HAPPY = "HAPPY", "Happy"
        NORMAL = "NORMAL", "Normal"
        TIRED = "TIRED", "Tired"
        UPSET = "UPSET", "Upset"

    class MealStatus(models.TextChoices):
        ATE_WELL = "ATE_WELL", "Ate well"
        ATE_SOME = "ATE_SOME", "Ate some"
        REFUSED = "REFUSED", "Refused"
        NOT_OFFERED = "NOT_OFFERED", "Not offered"

    class Participation(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        PARTIAL = "PARTIAL", "Partial"
        NONE = "NONE", "Did not participate"

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="daily_reports")
    date = models.DateField(db_index=True)
    mood = models.CharField(max_length=16, choices=Mood.choices)
    breakfast_status = models.CharField(max_length=16, choices=MealStatus.choices, default=MealStatus.NOT_OFFERED)
    lunch_status = models.CharField(max_length=16, choices=MealStatus.choices, default=MealStatus.NOT_OFFERED)
    snack_status = models.CharField(max_length=16, choices=MealStatus.choices, default=MealStatus.NOT_OFFERED)
    nap_duration = models.DurationField(null=True, blank=True)
    activity_participation = models.CharField(
        max_length=16,
        choices=Participation.choices,
        default=Participation.ACTIVE,
    )
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_daily_reports",
    )

    class Meta:
        ordering = ["-date", "child__last_name"]
        constraints = [
            models.UniqueConstraint(fields=["child", "date"], name="unique_daily_report_per_child_date"),
        ]
        indexes = [
            models.Index(fields=["child", "date"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self) -> str:
        return f"{self.child} {self.date}"

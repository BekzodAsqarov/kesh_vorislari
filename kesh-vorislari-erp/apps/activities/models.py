from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.groups.models import Group


class Activity(TimeStampedModel):
    class ActivityType(models.TextChoices):
        ART = "ART", "Art"
        MATH = "MATH", "Math"
        LANGUAGE = "LANGUAGE", "Language"
        PHYSICAL = "PHYSICAL", "Physical"
        MUSIC = "MUSIC", "Music"
        SCIENCE = "SCIENCE", "Science"
        READING = "READING", "Reading"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    activity_type = models.CharField(max_length=32, choices=ActivityType.choices, db_index=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="activities")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
        limit_choices_to={"role": "TEACHER"},
    )
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date", "start_time"]
        indexes = [
            models.Index(fields=["date", "group"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start_time__lte=models.F("end_time")),
                name="activity_start_before_end",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.date})"

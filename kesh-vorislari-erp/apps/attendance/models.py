from django.conf import settings
from django.db import models

from apps.children.models import Child
from apps.core.models import TimeStampedModel


class Attendance(TimeStampedModel):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"
        EXCUSED = "EXCUSED", "Excused"

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=16, choices=Status.choices)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recorded_attendance",
    )

    class Meta:
        ordering = ["-date", "child__last_name"]
        constraints = [
            models.UniqueConstraint(fields=["child", "date"], name="unique_attendance_per_child_date"),
        ]
        indexes = [
            models.Index(fields=["date", "status"]),
            models.Index(fields=["child", "date"]),
        ]

    def __str__(self) -> str:
        return f"{self.child} {self.date} {self.status}"

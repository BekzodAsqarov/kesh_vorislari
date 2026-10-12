from rest_framework import serializers

from apps.core.exceptions import DomainError

from .models import DailyReport
from .services import upsert_daily_report


class DailyReportSerializer(serializers.ModelSerializer):
    child_name = serializers.CharField(source="child.full_name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)

    class Meta:
        model = DailyReport
        fields = (
            "id",
            "child",
            "child_name",
            "date",
            "mood",
            "breakfast_status",
            "lunch_status",
            "snack_status",
            "nap_duration",
            "activity_participation",
            "note",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def create(self, validated_data):
        try:
            return upsert_daily_report(created_by=self.context["request"].user, date_value=validated_data.pop("date"), **validated_data)
        except DomainError as exc:
            raise serializers.ValidationError(str(exc)) from exc

    def update(self, instance, validated_data):
        try:
            return upsert_daily_report(
                child=validated_data.get("child", instance.child),
                date_value=validated_data.get("date", instance.date),
                created_by=self.context["request"].user,
                mood=validated_data.get("mood", instance.mood),
                breakfast_status=validated_data.get("breakfast_status", instance.breakfast_status),
                lunch_status=validated_data.get("lunch_status", instance.lunch_status),
                snack_status=validated_data.get("snack_status", instance.snack_status),
                activity_participation=validated_data.get(
                    "activity_participation", instance.activity_participation
                ),
                nap_duration=validated_data.get("nap_duration", instance.nap_duration),
                note=validated_data.get("note", instance.note),
            )
        except DomainError as exc:
            raise serializers.ValidationError(str(exc)) from exc

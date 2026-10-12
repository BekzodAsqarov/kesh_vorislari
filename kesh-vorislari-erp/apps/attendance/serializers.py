from rest_framework import serializers

from apps.children.models import Child
from apps.core.exceptions import DomainError
from apps.groups.models import Group

from .models import Attendance
from .services import bulk_record_attendance, record_attendance


class AttendanceSerializer(serializers.ModelSerializer):
    child_name = serializers.CharField(source="child.full_name", read_only=True)
    group_name = serializers.CharField(source="child.group.name", read_only=True)
    recorded_by_name = serializers.CharField(source="recorded_by.get_full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = (
            "id",
            "child",
            "child_name",
            "group_name",
            "date",
            "status",
            "arrival_time",
            "departure_time",
            "note",
            "recorded_by",
            "recorded_by_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "recorded_by", "created_at", "updated_at")

    def validate(self, attrs):
        arrival = attrs.get("arrival_time") or getattr(self.instance, "arrival_time", None)
        departure = attrs.get("departure_time") or getattr(self.instance, "departure_time", None)
        if arrival and departure and arrival > departure:
            raise serializers.ValidationError("Arrival time must be before departure time.")
        return attrs

    def create(self, validated_data):
        try:
            return record_attendance(
                child=validated_data["child"],
                date_value=validated_data["date"],
                status=validated_data["status"],
                recorded_by=self.context["request"].user,
                arrival_time=validated_data.get("arrival_time"),
                departure_time=validated_data.get("departure_time"),
                note=validated_data.get("note", ""),
            )
        except DomainError as exc:
            raise serializers.ValidationError(str(exc)) from exc

    def update(self, instance, validated_data):
        try:
            return record_attendance(
                child=validated_data.get("child", instance.child),
                date_value=validated_data.get("date", instance.date),
                status=validated_data.get("status", instance.status),
                recorded_by=self.context["request"].user,
                arrival_time=validated_data.get("arrival_time", instance.arrival_time),
                departure_time=validated_data.get("departure_time", instance.departure_time),
                note=validated_data.get("note", instance.note),
            )
        except DomainError as exc:
            raise serializers.ValidationError(str(exc)) from exc


class BulkAttendanceItemSerializer(serializers.Serializer):
    child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.all())
    status = serializers.ChoiceField(choices=Attendance.Status.choices)
    arrival_time = serializers.TimeField(required=False, allow_null=True)
    departure_time = serializers.TimeField(required=False, allow_null=True)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class BulkAttendanceSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    date = serializers.DateField()
    records = BulkAttendanceItemSerializer(many=True)

    def create(self, validated_data):
        try:
            items = bulk_record_attendance(
                group=validated_data["group"],
                date_value=validated_data["date"],
                records=validated_data["records"],
                recorded_by=self.context["request"].user,
            )
        except DomainError as exc:
            raise serializers.ValidationError(str(exc)) from exc
        return items

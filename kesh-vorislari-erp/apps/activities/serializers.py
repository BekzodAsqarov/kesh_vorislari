from rest_framework import serializers

from apps.core.exceptions import DomainError
from apps.groups.selectors import groups_for_user

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source="group.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.get_full_name", read_only=True)

    class Meta:
        model = Activity
        fields = (
            "id",
            "title",
            "description",
            "activity_type",
            "group",
            "group_name",
            "teacher",
            "teacher_name",
            "date",
            "start_time",
            "end_time",
            "location",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        group = attrs.get("group") or getattr(self.instance, "group", None)
        start = attrs.get("start_time") or getattr(self.instance, "start_time", None)
        end = attrs.get("end_time") or getattr(self.instance, "end_time", None)
        if start and end and start > end:
            raise serializers.ValidationError("Start time must be before end time.")
        if user.is_teacher and group and not groups_for_user(user).filter(pk=group.pk).exists():
            raise serializers.ValidationError("You can only manage activities for assigned groups.")
        if user.is_teacher:
            attrs.setdefault("teacher", user)
        return attrs

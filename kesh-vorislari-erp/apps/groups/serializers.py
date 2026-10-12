from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer

from .models import Group
from .services import create_group


class GroupSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True, read_only=True)
    teacher_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.TEACHER),
        many=True,
        write_only=True,
        required=False,
        source="teachers",
    )
    children_count = serializers.IntegerField(source="children.count", read_only=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "room",
            "age_min",
            "age_max",
            "teachers",
            "teacher_ids",
            "is_active",
            "children_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        teachers = validated_data.pop("teachers", [])
        return create_group(teachers=teachers, **validated_data)

    def update(self, instance, validated_data):
        teachers = validated_data.pop("teachers", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if teachers is not None:
            instance.teachers.set(teachers)
        return instance

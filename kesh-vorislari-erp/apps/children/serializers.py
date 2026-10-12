from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.groups.serializers import GroupSerializer

from .models import Child
from .services import create_child


class ChildSerializer(serializers.ModelSerializer):
    group_detail = GroupSerializer(source="group", read_only=True)
    parents_detail = UserSerializer(source="parents", many=True, read_only=True)
    parent_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.PARENT),
        many=True,
        write_only=True,
        required=False,
        source="parents",
    )
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Child
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "date_of_birth",
            "gender",
            "group",
            "group_detail",
            "parents",
            "parents_detail",
            "parent_ids",
            "contact_phone",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "allergies",
            "medical_notes",
            "enrollment_date",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "parents")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user and user.is_parent:
            data.pop("medical_notes", None)
            data.pop("address", None)
        return data

    def create(self, validated_data):
        parents = validated_data.pop("parents", [])
        return create_child(parents=parents, **validated_data)

    def update(self, instance, validated_data):
        parents = validated_data.pop("parents", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if parents is not None:
            instance.parents.set(parents)
        return instance

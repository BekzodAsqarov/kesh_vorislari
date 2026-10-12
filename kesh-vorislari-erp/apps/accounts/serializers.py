from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ParentProfile, TeacherProfile, User
from .services import create_user, update_user


class RoleAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ("qualification", "bio", "hire_date")


class ParentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentProfile
        fields = ("relationship", "secondary_phone", "address")


class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    parent_profile = ParentProfileSerializer(read_only=True)
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "phone",
            "is_active",
            "date_joined",
            "teacher_profile",
            "parent_profile",
        )
        read_only_fields = ("id", "date_joined")


class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    teacher_profile = TeacherProfileSerializer(required=False)
    parent_profile = ParentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
            "teacher_profile",
            "parent_profile",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": "Password is required."})
        return attrs

    def create(self, validated_data):
        teacher_data = validated_data.pop("teacher_profile", {}) or {}
        parent_data = validated_data.pop("parent_profile", {}) or {}
        profile = teacher_data if validated_data["role"] == User.Role.TEACHER else parent_data
        return create_user(**validated_data, **profile)

    def update(self, instance, validated_data):
        validated_data.pop("teacher_profile", None)
        validated_data.pop("parent_profile", None)
        return update_user(instance, **validated_data)

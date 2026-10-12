from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ParentProfile, TeacherProfile, User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "role")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    extra = 0


class ParentProfileInline(admin.StackedInline):
    model = ParentProfile
    extra = 0


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)
    readonly_fields = ("created_at", "updated_at", "date_joined", "last_login")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("first_name", "last_name", "phone", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Timestamps", {"fields": ("date_joined", "last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
            },
        ),
    )

    def get_inlines(self, request, obj=None):
        if obj and obj.role == User.Role.TEACHER:
            return [TeacherProfileInline]
        if obj and obj.role == User.Role.PARENT:
            return [ParentProfileInline]
        return []

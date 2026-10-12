from django.contrib import admin

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "room", "age_min", "age_max", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "room", "description")
    ordering = ("name",)
    filter_horizontal = ("teachers",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("teachers",)
    fieldsets = (
        (None, {"fields": ("name", "description", "room", "is_active")}),
        ("Age range", {"fields": ("age_min", "age_max")}),
        ("Teachers", {"fields": ("teachers",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

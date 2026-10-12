from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "activity_type", "group", "teacher", "date", "start_time", "end_time")
    list_filter = ("activity_type", "date", "group")
    search_fields = ("title", "description", "location")
    ordering = ("-date", "start_time")
    date_hierarchy = "date"
    autocomplete_fields = ("group", "teacher")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "description", "activity_type")}),
        ("Schedule", {"fields": ("group", "teacher", "date", "start_time", "end_time", "location")}),
        ("Notes", {"fields": ("notes",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

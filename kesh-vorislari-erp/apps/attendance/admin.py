from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("date", "child", "status", "arrival_time", "departure_time", "recorded_by")
    list_filter = ("status", "date")
    search_fields = ("child__first_name", "child__last_name", "note")
    ordering = ("-date",)
    autocomplete_fields = ("child", "recorded_by")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "date"

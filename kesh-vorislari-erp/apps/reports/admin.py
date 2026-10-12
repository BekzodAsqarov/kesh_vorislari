from django.contrib import admin

from .models import DailyReport


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ("date", "child", "mood", "breakfast_status", "lunch_status", "created_by")
    list_filter = ("mood", "date")
    search_fields = ("child__first_name", "child__last_name", "note")
    ordering = ("-date",)
    date_hierarchy = "date"
    autocomplete_fields = ("child", "created_by")
    readonly_fields = ("created_at", "updated_at")

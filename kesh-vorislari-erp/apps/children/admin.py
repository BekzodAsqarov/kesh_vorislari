from django.contrib import admin

from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "group", "gender", "date_of_birth", "is_active")
    list_filter = ("is_active", "gender", "group")
    search_fields = ("first_name", "last_name", "allergies", "emergency_contact_name")
    ordering = ("last_name", "first_name")
    autocomplete_fields = ("group", "parents")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Identity", {"fields": ("first_name", "last_name", "date_of_birth", "gender")}),
        ("Enrollment", {"fields": ("group", "parents", "enrollment_date", "is_active")}),
        ("Contact", {"fields": ("contact_phone", "address", "emergency_contact_name", "emergency_contact_phone")}),
        ("Health", {"fields": ("allergies", "medical_notes")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

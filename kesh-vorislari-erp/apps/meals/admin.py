from django.contrib import admin

from .models import Meal, Menu, MenuItem


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "allergens", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "ingredients", "allergens")
    ordering = ("category", "name")
    readonly_fields = ("created_at", "updated_at")


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    autocomplete_fields = ("meal",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("date", "created_by", "notes")
    list_filter = ("date",)
    search_fields = ("notes", "items__name")
    ordering = ("-date",)
    date_hierarchy = "date"
    inlines = [MenuItemInline]
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("created_by",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("menu", "category", "name", "allergens")
    list_filter = ("category",)
    search_fields = ("name", "ingredients", "allergens")
    autocomplete_fields = ("menu", "meal")
    readonly_fields = ("created_at", "updated_at")

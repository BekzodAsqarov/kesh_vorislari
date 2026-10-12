from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class MealCategory(models.TextChoices):
    BREAKFAST = "BREAKFAST", "Breakfast"
    SECOND_BREAKFAST = "SECOND_BREAKFAST", "Second breakfast"
    LUNCH = "LUNCH", "Lunch"
    SNACK = "SNACK", "Snack"


class Meal(TimeStampedModel):
    """Reusable dish in the kitchen catalog."""

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=32, choices=MealCategory.choices, db_index=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    allergens = models.CharField(max_length=255, blank=True)
    portion = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]
        unique_together = [("name", "category")]

    def __str__(self) -> str:
        return f"{self.get_category_display()}: {self.name}"


class Menu(TimeStampedModel):
    date = models.DateField(unique=True, db_index=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_menus",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Menu {self.date}"


class MenuItem(TimeStampedModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True, related_name="menu_items")
    category = models.CharField(max_length=32, choices=MealCategory.choices, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    allergens = models.CharField(max_length=255, blank=True)
    portion = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["menu__date", "category", "sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.menu.date} {self.category}: {self.name}"

    def save(self, *args, **kwargs):
        if self.meal and not self.name:
            self.name = self.meal.name
            self.category = self.meal.category
            self.description = self.description or self.meal.description
            self.ingredients = self.ingredients or self.meal.ingredients
            self.allergens = self.allergens or self.meal.allergens
            self.portion = self.portion or self.meal.portion
        super().save(*args, **kwargs)

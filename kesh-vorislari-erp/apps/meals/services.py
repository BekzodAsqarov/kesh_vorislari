from datetime import date

from django.db import transaction

from apps.accounts.models import User

from .models import Meal, Menu, MenuItem


@transaction.atomic
def create_menu(*, menu_date: date, created_by: User, notes: str = "", items: list[dict] | None = None) -> Menu:
    menu = Menu.objects.create(date=menu_date, notes=notes, created_by=created_by)
    for index, item in enumerate(items or []):
        meal = item.get("meal")
        MenuItem.objects.create(
            menu=menu,
            meal=meal,
            category=item.get("category") or (meal.category if meal else None),
            name=item.get("name") or (meal.name if meal else ""),
            description=item.get("description", "") or (meal.description if meal else ""),
            ingredients=item.get("ingredients", "") or (meal.ingredients if meal else ""),
            allergens=item.get("allergens", "") or (meal.allergens if meal else ""),
            portion=item.get("portion", "") or (meal.portion if meal else ""),
            notes=item.get("notes", ""),
            sort_order=item.get("sort_order", index),
        )
    return menu


def upsert_meal(**fields) -> Meal:
    meal, _created = Meal.objects.update_or_create(
        name=fields["name"],
        category=fields["category"],
        defaults={k: v for k, v in fields.items() if k not in {"name", "category"}},
    )
    return meal

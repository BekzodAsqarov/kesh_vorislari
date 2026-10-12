from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.services import create_user
from apps.meals.models import MealCategory


class MenuTests(APITestCase):
    def setUp(self):
        self.admin = create_user(
            email="admin@test.local", password="x", first_name="A", last_name="A", role=User.Role.ADMIN
        )
        self.parent = create_user(
            email="p@test.local", password="x", first_name="P", last_name="P", role=User.Role.PARENT
        )

    def test_admin_can_create_menu(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/meals/menus/",
            {
                "date": "2026-10-08",
                "notes": "Autumn menu",
                "items": [
                    {"name": "Mastava", "category": MealCategory.LUNCH, "allergens": ""},
                    {"name": "Non", "category": MealCategory.LUNCH, "allergens": "Gluten"},
                ],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["items"]), 2)

    def test_parent_can_view_menus_but_not_create(self):
        self.client.force_authenticate(self.admin)
        self.client.post(
            "/api/meals/menus/",
            {"date": "2026-10-08", "items": [{"name": "Choy", "category": MealCategory.BREAKFAST}]},
            format="json",
        )
        self.client.force_authenticate(self.parent)
        listing = self.client.get("/api/meals/menus/")
        self.assertEqual(listing.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(listing.data["count"], 1)
        create = self.client.post(
            "/api/meals/menus/",
            {"date": "2026-10-09", "items": [{"name": "Sok", "category": MealCategory.SNACK}]},
            format="json",
        )
        self.assertEqual(create.status_code, status.HTTP_403_FORBIDDEN)

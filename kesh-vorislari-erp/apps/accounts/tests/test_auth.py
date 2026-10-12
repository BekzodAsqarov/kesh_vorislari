from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.services import create_user


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.admin = create_user(
            email="admin@test.local",
            password="Admin123!",
            first_name="Ada",
            last_name="Admin",
            role=User.Role.ADMIN,
        )
        self.teacher = create_user(
            email="teacher@test.local",
            password="Teacher123!",
            first_name="Tim",
            last_name="Teacher",
            role=User.Role.TEACHER,
        )

    def test_login_returns_tokens(self):
        response = self.client.post(
            reverse("api-login"),
            {"email": "admin@test.local", "password": "Admin123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["role"], User.Role.ADMIN)

    def test_me_requires_authentication(self):
        response = self.client.get(reverse("api-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_profile(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.get(reverse("api-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "teacher@test.local")

    def test_teacher_cannot_list_users(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.get("/api/auth/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

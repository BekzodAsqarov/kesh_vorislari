from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.services import create_user
from apps.children.models import Child
from apps.groups.models import Group


class ChildPermissionTests(APITestCase):
    def setUp(self):
        self.admin = create_user(
            email="admin@test.local", password="x", first_name="A", last_name="A", role=User.Role.ADMIN
        )
        self.teacher_a = create_user(
            email="ta@test.local", password="x", first_name="T", last_name="A", role=User.Role.TEACHER
        )
        self.teacher_b = create_user(
            email="tb@test.local", password="x", first_name="T", last_name="B", role=User.Role.TEACHER
        )
        self.parent_a = create_user(
            email="pa@test.local", password="x", first_name="P", last_name="A", role=User.Role.PARENT
        )
        self.parent_b = create_user(
            email="pb@test.local", password="x", first_name="P", last_name="B", role=User.Role.PARENT
        )
        self.group_a = Group.objects.create(name="Quyoshcha", age_min=3, age_max=4)
        self.group_b = Group.objects.create(name="Katta guruh", age_min=5, age_max=6)
        self.group_a.teachers.add(self.teacher_a)
        self.group_b.teachers.add(self.teacher_b)
        self.child_a = Child.objects.create(
            first_name="Asal",
            last_name="Rahimova",
            date_of_birth=date(2021, 1, 1),
            gender=Child.Gender.FEMALE,
            group=self.group_a,
            enrollment_date=date(2025, 9, 1),
        )
        self.child_a.parents.add(self.parent_a)
        self.child_b = Child.objects.create(
            first_name="Jasur",
            last_name="Usmanov",
            date_of_birth=date(2020, 1, 1),
            gender=Child.Gender.MALE,
            group=self.group_b,
            enrollment_date=date(2025, 9, 1),
        )
        self.child_b.parents.add(self.parent_b)

    def test_admin_can_create_child(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/children/",
            {
                "first_name": "Omar",
                "last_name": "Karimov",
                "date_of_birth": "2021-05-05",
                "gender": Child.Gender.MALE,
                "group": self.group_a.pk,
                "enrollment_date": "2025-09-01",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_see_unrelated_child(self):
        self.client.force_authenticate(self.teacher_a)
        response = self.client.get("/api/children/")
        ids = [row["id"] for row in response.data["results"]]
        self.assertIn(self.child_a.pk, ids)
        self.assertNotIn(self.child_b.pk, ids)

    def test_parent_sees_only_own_children(self):
        self.client.force_authenticate(self.parent_a)
        response = self.client.get("/api/children/")
        ids = [row["id"] for row in response.data["results"]]
        self.assertEqual(ids, [self.child_a.pk])
        forbidden = self.client.get(f"/api/children/{self.child_b.pk}/")
        self.assertEqual(forbidden.status_code, status.HTTP_404_NOT_FOUND)

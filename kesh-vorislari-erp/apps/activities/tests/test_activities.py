from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.services import create_user
from apps.activities.models import Activity
from apps.groups.models import Group


class ActivityTests(APITestCase):
    def setUp(self):
        self.admin = create_user(
            email="admin@test.local", password="x", first_name="A", last_name="A", role=User.Role.ADMIN
        )
        self.teacher = create_user(
            email="t@test.local", password="x", first_name="T", last_name="T", role=User.Role.TEACHER
        )
        self.other = create_user(
            email="o@test.local", password="x", first_name="O", last_name="O", role=User.Role.TEACHER
        )
        self.group = Group.objects.create(name="Quyoshcha", age_min=3, age_max=4)
        self.other_group = Group.objects.create(name="Other", age_min=5, age_max=6)
        self.group.teachers.add(self.teacher)
        self.other_group.teachers.add(self.other)

    def test_admin_can_create_activity(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/activities/",
            {
                "title": "Rasm chizish",
                "activity_type": Activity.ActivityType.ART,
                "group": self.group.pk,
                "teacher": self.teacher.pk,
                "date": "2026-10-08",
                "start_time": "09:00:00",
                "end_time": "09:40:00",
                "location": "Art room",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_create_for_unassigned_group(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            "/api/activities/",
            {
                "title": "Musiqa",
                "activity_type": Activity.ActivityType.MUSIC,
                "group": self.other_group.pk,
                "date": "2026-10-08",
                "start_time": "10:00:00",
                "end_time": "10:30:00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from datetime import date

from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.accounts.services import create_user
from apps.attendance.models import Attendance
from apps.children.models import Child
from apps.groups.models import Group


class AttendanceTests(APITestCase):
    def setUp(self):
        self.admin = create_user(
            email="admin@test.local", password="x", first_name="A", last_name="A", role=User.Role.ADMIN
        )
        self.teacher = create_user(
            email="t@test.local", password="x", first_name="T", last_name="T", role=User.Role.TEACHER
        )
        self.other_teacher = create_user(
            email="t2@test.local", password="x", first_name="O", last_name="T", role=User.Role.TEACHER
        )
        self.group = Group.objects.create(name="Bilimdonlar", age_min=4, age_max=5)
        self.other_group = Group.objects.create(name="Other", age_min=3, age_max=4)
        self.group.teachers.add(self.teacher)
        self.other_group.teachers.add(self.other_teacher)
        self.child = Child.objects.create(
            first_name="Madina",
            last_name="Usmanova",
            date_of_birth=date(2020, 1, 1),
            gender=Child.Gender.FEMALE,
            group=self.group,
            enrollment_date=date(2025, 9, 1),
        )

    def test_create_attendance(self):
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            "/api/attendance/",
            {"child": self.child.pk, "date": "2026-10-08", "status": Attendance.Status.PRESENT},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.filter(child=self.child, date="2026-10-08").count(), 1)

    def test_duplicate_attendance_does_not_create_second_row(self):
        self.client.force_authenticate(self.admin)
        payload = {"child": self.child.pk, "date": "2026-10-08", "status": Attendance.Status.PRESENT}
        self.client.post("/api/attendance/", payload, format="json")
        payload["status"] = Attendance.Status.LATE
        self.client.post("/api/attendance/", payload, format="json")
        self.assertEqual(Attendance.objects.filter(child=self.child, date="2026-10-08").count(), 1)
        with self.assertRaises(IntegrityError):
            Attendance.objects.create(
                child=self.child,
                date=date(2026, 10, 8),
                status=Attendance.Status.ABSENT,
            )

    def test_teacher_cannot_mark_other_group(self):
        outsider = Child.objects.create(
            first_name="Bek",
            last_name="Ali",
            date_of_birth=date(2020, 2, 2),
            gender=Child.Gender.MALE,
            group=self.other_group,
            enrollment_date=date(2025, 9, 1),
        )
        self.client.force_authenticate(self.teacher)
        response = self.client.post(
            "/api/attendance/",
            {"child": outsider.pk, "date": "2026-10-08", "status": Attendance.Status.PRESENT},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

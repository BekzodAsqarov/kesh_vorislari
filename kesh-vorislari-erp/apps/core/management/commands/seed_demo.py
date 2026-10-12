from datetime import date, time, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.accounts.services import create_user
from apps.activities.models import Activity
from apps.attendance.models import Attendance
from apps.attendance.services import record_attendance
from apps.children.models import Child
from apps.children.services import create_child
from apps.groups.models import Group
from apps.meals.models import Meal, MealCategory, Menu, MenuItem
from apps.reports.models import DailyReport
from apps.reports.services import upsert_daily_report


class Command(BaseCommand):
    help = "Create realistic development data. Never use these passwords in production."

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.localdate()
        admin = User.objects.filter(email="admin@keshvorislari.local").first()
        if not admin:
            admin = create_user(
                email="admin@keshvorislari.local",
                password="Admin123!",
                first_name="Malika",
                last_name="Karimova",
                role=User.Role.ADMIN,
                phone="+998901111111",
            )
        else:
            admin.set_password("Admin123!")
            admin.save()

        teacher_nilufar = self._user(
            "teacher.nilufar@keshvorislari.local",
            "Teacher123!",
            "Nilufar",
            "Saidova",
            User.Role.TEACHER,
            qualification="Early childhood educator",
        )
        teacher_javlon = self._user(
            "teacher.javlon@keshvorislari.local",
            "Teacher123!",
            "Javlon",
            "Tursunov",
            User.Role.TEACHER,
            qualification="Physical education",
        )
        parent_dilnoza = self._user(
            "parent.dilnoza@keshvorislari.local",
            "Parent123!",
            "Dilnoza",
            "Rahimova",
            User.Role.PARENT,
            relationship="Mother",
        )
        parent_aziz = self._user(
            "parent.aziz@keshvorislari.local",
            "Parent123!",
            "Aziz",
            "Usmanov",
            User.Role.PARENT,
            relationship="Father",
        )
        parent_sevara = self._user(
            "parent.sevara@keshvorislari.local",
            "Parent123!",
            "Sevara",
            "Yuldasheva",
            User.Role.PARENT,
            relationship="Mother",
        )

        quyoshcha, _ = Group.objects.update_or_create(
            name="Quyoshcha",
            defaults={"description": "Younger group", "room": "101", "age_min": 3, "age_max": 4, "is_active": True},
        )
        bilimdonlar, _ = Group.objects.update_or_create(
            name="Bilimdonlar",
            defaults={"description": "Middle group", "room": "102", "age_min": 4, "age_max": 5, "is_active": True},
        )
        katta, _ = Group.objects.update_or_create(
            name="Katta guruh",
            defaults={"description": "Older group", "room": "201", "age_min": 5, "age_max": 6, "is_active": True},
        )
        quyoshcha.teachers.set([teacher_nilufar])
        bilimdonlar.teachers.set([teacher_nilufar, teacher_javlon])
        katta.teachers.set([teacher_javlon])

        children_spec = [
            ("Asal", "Rahimova", date(2021, 3, 12), Child.Gender.FEMALE, quyoshcha, [parent_dilnoza]),
            ("Omar", "Rahimov", date(2021, 8, 2), Child.Gender.MALE, quyoshcha, [parent_dilnoza]),
            ("Madina", "Usmanova", date(2020, 11, 20), Child.Gender.FEMALE, bilimdonlar, [parent_aziz]),
            ("Sardor", "Usmanov", date(2020, 5, 9), Child.Gender.MALE, bilimdonlar, [parent_aziz]),
            ("Laylo", "Yuldasheva", date(2019, 4, 18), Child.Gender.FEMALE, katta, [parent_sevara]),
            ("Jasur", "Yuldashev", date(2019, 9, 1), Child.Gender.MALE, katta, [parent_sevara]),
            ("Nigora", "Karimova", date(2021, 1, 30), Child.Gender.FEMALE, quyoshcha, [parent_dilnoza]),
            ("Bekzod", "Toshpulatov", date(2020, 2, 14), Child.Gender.MALE, bilimdonlar, [parent_aziz]),
        ]
        children = []
        for first, last, dob, gender, group, parents in children_spec:
            child = Child.objects.filter(first_name=first, last_name=last).first()
            if not child:
                child = create_child(
                    first_name=first,
                    last_name=last,
                    date_of_birth=dob,
                    gender=gender,
                    group=group,
                    enrollment_date=date(2025, 9, 1),
                    parents=parents,
                    contact_phone="+998901234567",
                    address="Shahrisabz, Kesh",
                    emergency_contact_name=parents[0].get_full_name(),
                    emergency_contact_phone=parents[0].phone or "+998909999999",
                    allergies="Peanuts" if first == "Asal" else "",
                    medical_notes="",
                )
            else:
                child.group = group
                child.save()
                child.parents.set(parents)
            children.append(child)

        meals = [
            ("Sutli bo'tqa", MealCategory.BREAKFAST, "Milk porridge", "Milk, rice, sugar", "Milk"),
            ("Non", MealCategory.BREAKFAST, "Bread", "Wheat, yeast", "Gluten"),
            ("Choy", MealCategory.BREAKFAST, "Tea", "Black tea", ""),
            ("Olma", MealCategory.SECOND_BREAKFAST, "Apple", "Apple", ""),
            ("Sok", MealCategory.SECOND_BREAKFAST, "Juice", "Fruit", ""),
            ("Mastava", MealCategory.LUNCH, "Rice soup", "Rice, beef, vegetables", ""),
            ("Salat", MealCategory.LUNCH, "Salad", "Cucumber, tomato", ""),
            ("Kefir", MealCategory.SNACK, "Kefir", "Fermented milk", "Milk"),
            ("Pechenye", MealCategory.SNACK, "Cookies", "Flour, sugar", "Gluten"),
        ]
        meal_objs = []
        for name, category, desc, ingredients, allergens in meals:
            meal, _ = Meal.objects.update_or_create(
                name=name,
                category=category,
                defaults={"description": desc, "ingredients": ingredients, "allergens": allergens, "portion": "1 serving"},
            )
            meal_objs.append(meal)

        for offset in range(5):
            menu_date = today - timedelta(days=offset)
            menu, _ = Menu.objects.update_or_create(date=menu_date, defaults={"notes": "Seasonal kindergarten menu", "created_by": admin})
            menu.items.all().delete()
            for meal in meal_objs:
                MenuItem.objects.create(
                    menu=menu,
                    meal=meal,
                    category=meal.category,
                    name=meal.name,
                    description=meal.description,
                    ingredients=meal.ingredients,
                    allergens=meal.allergens,
                    portion=meal.portion,
                )

        statuses = [Attendance.Status.PRESENT, Attendance.Status.PRESENT, Attendance.Status.LATE, Attendance.Status.ABSENT]
        for child, status in zip(children, statuses * 3):
            record_attendance(
                child=child,
                date_value=today,
                status=status,
                recorded_by=admin,
                arrival_time=time(8, 10) if status != Attendance.Status.ABSENT else None,
            )

        activities = [
            ("Rasm chizish", Activity.ActivityType.ART, quyoshcha, teacher_nilufar, time(9, 0), time(9, 40), "Art room"),
            ("Matematika", Activity.ActivityType.MATH, bilimdonlar, teacher_nilufar, time(10, 0), time(10, 40), "102"),
            ("Jismoniy tarbiya", Activity.ActivityType.PHYSICAL, katta, teacher_javlon, time(11, 0), time(11, 40), "Hall"),
            ("Musiqa", Activity.ActivityType.MUSIC, bilimdonlar, teacher_javlon, time(15, 0), time(15, 30), "Music room"),
            ("Kitob o'qish", Activity.ActivityType.READING, quyoshcha, teacher_nilufar, time(16, 0), time(16, 30), "Library corner"),
        ]
        for title, atype, group, teacher, start, end, location in activities:
            Activity.objects.update_or_create(
                title=title,
                date=today,
                group=group,
                defaults={
                    "description": title,
                    "activity_type": atype,
                    "teacher": teacher,
                    "start_time": start,
                    "end_time": end,
                    "location": location,
                },
            )

        moods = [DailyReport.Mood.HAPPY, DailyReport.Mood.NORMAL, DailyReport.Mood.TIRED]
        for index, child in enumerate(children):
            upsert_daily_report(
                child=child,
                date_value=today,
                created_by=teacher_nilufar if child.group in {quyoshcha, bilimdonlar} else teacher_javlon,
                mood=moods[index % 3],
                breakfast_status=DailyReport.MealStatus.ATE_WELL,
                lunch_status=DailyReport.MealStatus.ATE_SOME,
                snack_status=DailyReport.MealStatus.ATE_WELL,
                activity_participation=DailyReport.Participation.ACTIVE,
                nap_duration=timedelta(hours=1, minutes=20),
                note="Participated well in group activities.",
            )

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write("Admin:   admin@keshvorislari.local / Admin123!")
        self.stdout.write("Teacher: teacher.nilufar@keshvorislari.local / Teacher123!")
        self.stdout.write("Parent:  parent.dilnoza@keshvorislari.local / Parent123!")

    def _user(self, email, password, first, last, role, **profile):
        user = User.objects.filter(email=email).first()
        if not user:
            return create_user(
                email=email,
                password=password,
                first_name=first,
                last_name=last,
                role=role,
                phone="+99890" + email[8:12].ljust(7, "0")[:7],
                **profile,
            )
        user.set_password(password)
        user.save()
        return user

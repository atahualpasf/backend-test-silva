"""Load initial data command"""
# flake8: noqa
# Django
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.query_utils import Q
from django.utils import timezone

# Backend test
from backend_test.menus.models import Meal, Menu
from backend_test.users.models import Employee, User


class Command(BaseCommand):
    help = "Create dummy data."
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            help="Users number to be created. Greatear or equal to 5 else default. Default 10",
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "--meals",
            type=int,
            help="Meals number to be created. Greater or equal to 5 else default. Default 10",
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "--menus",
            type=int,
            help="Menus number to be created. Greater or equal to 5 else default. Default 10",
        )

    def handle(self, *args, **options):
        users_number = options.get("users")
        users_number = users_number if users_number and users_number >= 5 else 11
        meals_number = options.get("meals")
        meals_number = meals_number if meals_number and meals_number >= 5 else 11
        menus_number = options.get("menus")
        menus_number = menus_number if menus_number and menus_number >= 5 else 11

        with transaction.atomic():
            for i in range(1, users_number):
                user = User.objects.create_user(
                    email=f"demo{i}@demo.com",
                    password=f"demo{i}123456",
                    username=f"demo{i}",
                    first_name=f"Demo {i}",
                    last_name=f"Demo {i}",
                )

                if not i % 2:
                    Employee.objects.create(user=user)

            for i in range(1, meals_number):
                Meal.objects.create(name=f"Meal number {i}")
                pass

            for i in range(1, menus_number):
                Menu.objects.create(date=timezone.now() + timezone.timedelta(days=i))
                pass

            meal_coordinator_group, created = Group.objects.get_or_create(
                name="meal_coordinator"
            )
            permisions = (
                Permission.objects.filter(
                    Q(content_type__model="menu")
                    | Q(content_type__model="meal")
                    | Q(content_type__model="menuoption")
                    | Q(content_type__model="order", codename="view_order")
                    | Q(content_type__model="menu", codename="send_slack_reminder")
                )
                .order_by("id")
                .all()
            )
            meal_coordinator_group.permissions.set(permisions)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully data loaded. Total: {users_number - 1} Users, {int(users_number/2)} Employees, {meals_number - 1} Meals, {menus_number - 1} Menus"
            )
        )

"""Users models test."""

# fmt: off

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase

# Backend test
from backend_test.users.models.employees import Employee
from backend_test.utils.models import SoftDeleteModel, TimeStampedModel

# fmt: on

User = get_user_model()


class TestUserModel(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(email="test@test.com", password="test")
        user_from_database = User.objects.get(pk=user.pk)

        assert user.email == user_from_database.email

    def test_user_to_string_representation(self):
        user = User.objects.first()
        assert str(user) == user.email

    def test_user_manager_raises__create_error_on_none_password(self):
        with self.assertRaises(ValueError):
            User.objects._create_user(email="test", password=None)

    def test_user_manager_create_raises_error_on_none_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="test")

    def test_super_user_creation(self):
        user = User.objects.create_superuser(email="test@test.com", password="test")
        user_from_database = User.objects.get(pk=user.pk)

        assert user.is_staff
        assert user.is_superuser
        assert user.email == user_from_database.email


class TestEmployeeModel:
    def test_employee_subclasses(self, random_employee):
        assert isinstance(random_employee, TimeStampedModel)
        assert isinstance(random_employee, SoftDeleteModel)

    def test_user_to_string_representation(self, random_employee):
        assert str(random_employee) == str(random_employee.pk)

    def test_employee_soft_delete(self, random_employee):
        employees_total = Employee.objects.count()
        random_employee.soft_delete()
        employees_available_total = Employee.available_objects.count()
        random_employee_in_database = Employee.objects.get(pk=random_employee.pk)
        assert random_employee_in_database.is_deleted
        assert employees_total > employees_available_total
        assert employees_total == employees_available_total + 1

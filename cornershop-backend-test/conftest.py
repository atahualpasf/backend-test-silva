"""Tests configuration file."""
# fmt: off
# Pytest
import pytest
# Django
from django.contrib.auth import get_user_model
from django.core.management import call_command

from backend_test.menus.models.menus import Menu
from backend_test.users.models.employees import Employee

# fmt: on
User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("createdummydata")


@pytest.fixture
def random_user(db) -> User:
    return User.objects.first()


@pytest.fixture
def random_employee(db) -> Employee:
    return Employee.objects.first()


@pytest.fixture
def random_menu(db) -> Menu:
    return Menu.objects.first()

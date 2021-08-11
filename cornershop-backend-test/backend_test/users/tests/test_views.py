"""Users models test."""

# fmt: off
# Python
import pytest
from django.contrib.auth import logout
from django.http import response
# Django
from django.test import TestCase
from django.urls import reverse

# Pytest django
from pytest_django.asserts import assertTemplateUsed

# Django
from backend_test.users.models.users import User

# fmt: on


@pytest.fixture
def random_user(db) -> User:
    return User.objects.first()


@pytest.fixture(scope="class")
def login_class_conf(db, client) -> User:
    url = reverse("users:login")


@pytest.mark.parametrize("login_url", [reverse("users:login")])
class TestLoginView:
    def test_page_status_200(self, db, client, login_url):
        response = client.get(login_url)
        assert response.status_code == 200

    def test_page_uses_correct_template(self, db, client, login_url):
        response = client.get(login_url)
        assertTemplateUsed(response, "users/login.html")


@pytest.mark.parametrize("users_index_url", [reverse("users:index")])
class TestIndexView:
    def test_page_unauthenticated_status_302(self, db, client, users_index_url):
        response = client.get(users_index_url)
        assert response.status_code == 302

    def test_page_authenticated_status_200(self, client, users_index_url, random_user):
        client.force_login(random_user)
        response = client.get(users_index_url)
        assert response.status_code == 200

    def test_page_authenticated_status_200(self, client, users_index_url, random_user):
        client.force_login(random_user)
        response = client.get(users_index_url)
        assertTemplateUsed(response, "users/index.html")

"""Orders views test."""

# fmt: off
# Django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Backend test
from backend_test.menus.models.menus import Menu

# fmt: on

User = get_user_model()


class TestGenerateOrderView(TestCase):
    def setUp(self) -> None:
        self.orders_generate_url = reverse("orders:generate")
        self.login_url = reverse("users:login")
        self.user = User.objects.first()
        self.menu = Menu.objects.first()
        return super().setUp()

    def test_page_with_user_no_authenticated(self):
        response = self.client.post(self.orders_generate_url)
        assert response.status_code == 302
        assert self.login_url in response.url

    def test_page_user_authenticated_without_menu(self):
        self.client.login(username="demo1@demo.com", password="demo1123456")
        response = self.client.post(self.orders_generate_url)
        self.assertTemplateUsed(response, "orders/error.html")
        self.assertContains(response, "An error has occurred processing your request.")

"""Orders app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersAppConfig(AppConfig):
    """Orders app config."""

    name = "backend_test.orders"
    verbose_name = _("Orders")

"""Menus app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MenusAppConfig(AppConfig):
    """Menus app config."""

    name = "backend_test.menus"
    verbose_name = _("Menus")

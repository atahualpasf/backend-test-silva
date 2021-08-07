"""Locations app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsAppConfig(AppConfig):
    """Locations app config."""

    name = "backend_test.locations"
    verbose_name = _("Locations")

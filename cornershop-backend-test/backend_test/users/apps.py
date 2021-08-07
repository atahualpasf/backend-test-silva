"""Users app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsAppConfig(AppConfig):
    """Users app config."""

    name = "backend_test.users"
    verbose_name = _("Users")

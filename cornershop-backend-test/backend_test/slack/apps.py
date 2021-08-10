"""Slack app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SlackAppConfig(AppConfig):
    """Slack app config."""

    name = "backend_test.slack"
    verbose_name = _("Slack")

"""Users apps test."""

# Django
from django.apps import AppConfig, apps


def test_apps_instance_config():
    config = apps.get_app_config("users")
    assert isinstance(config, AppConfig)

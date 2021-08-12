"""Menus apps test."""

# Django
from django.apps import AppConfig, apps


def test_apps_instance_config():
    config = apps.get_app_config("menus")
    assert isinstance(config, AppConfig)

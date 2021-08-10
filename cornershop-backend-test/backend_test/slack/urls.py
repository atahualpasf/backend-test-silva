"""Slack urls."""

# Django
from django.urls import path

# Backend test
from backend_test.slack import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
]

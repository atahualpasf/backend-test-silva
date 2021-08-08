"""Users models."""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    """
    User model class.

    Extend from Django's Abstract User for default Django's user and
    TimeStampedModel for default timestamp fields. Additionally add some
    extra fields.
    """

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "password"]

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    def __str__(self) -> str:
        """Return username like a instance string representation"""
        return self.username

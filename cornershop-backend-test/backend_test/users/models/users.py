"""Users models."""

# Django
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.models import TimeStampedModel


class UserManager(UserManager):
    """Custom user manager to handle users creation"""

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have password")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(TimeStampedModel, AbstractUser):
    """
    User model class.

    Extend from Django's Abstract User for default Django's user and
    TimeStampedModel for default timestamp fields. Additionally add some
    extra fields.
    """

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    def __str__(self) -> str:
        """Return email like a instance string representation"""
        return self.email

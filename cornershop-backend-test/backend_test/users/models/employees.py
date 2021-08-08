"""Employees models."""

# Django
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.locations.models import Location
from backend_test.utils.models import SoftDeleteModel, TimeStampedModel


class Employee(TimeStampedModel, SoftDeleteModel):
    """
    Employee model class.

    Extend from TimeStampedModel for default timestamp fields and
    SoftDeleteModel for handling soft delete. Additionally add some
    extra fields.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.PROTECT,
        related_name="employees",
        related_query_name="employee",
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        on_delete=models.PROTECT,
        related_name="employees",
        related_query_name="employee",
    )
    slack_username = models.CharField(
        _("slack username"),
        unique=True,
        error_messages={
            "unique": "A employee with that slack username already exists."
        },
        max_length=50,
    )

    class Meta:
        """Meta options."""

        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    def __str__(self) -> str:
        """Return instance string representation"""
        return f"{self.pk}: {self.slack_username}"

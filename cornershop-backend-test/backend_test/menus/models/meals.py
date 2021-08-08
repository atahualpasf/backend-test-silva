"""Meals models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.models import SoftDeleteModel, TimeStampedModel


class Meal(TimeStampedModel, SoftDeleteModel):
    """
    Meal model class.

    Extend from TimeStampedModel for default timestamp fields and
    SoftDeleteModel for handling soft delete. Additionally add some
    extra fields.
    """

    name = models.CharField(
        _("name"),
        max_length=255,
    )

    class Meta(TimeStampedModel.Meta):
        """Meta options."""

        verbose_name = _("meal")
        verbose_name_plural = _("meals")

    def __str__(self) -> str:
        """Return instance string representation"""
        return "{}: {}{too_long}".format(
            self.pk, self.name[0:25], too_long="..." if len(self.name) > 25 else ""
        )

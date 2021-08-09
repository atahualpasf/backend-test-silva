"""Menus models."""

# Python
import uuid

# Django
from django.core.validators import MinValueValidator
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.models import SoftDeleteModel, TimeStampedModel


def generate_unique_uuid():
    tmp_uuid = str(uuid.uuid4())
    while Menu.objects.filter(uuid=tmp_uuid).exists():
        tmp_uuid = str(uuid.uuid4())
    return tmp_uuid


class Menu(TimeStampedModel, SoftDeleteModel):
    """
    Menu model class.

    Extend from TimeStampedModel for default timestamp fields and
    SoftDeleteModel for handling soft delete. Additionally add some
    extra fields.
    """

    uuid = models.UUIDField(unique=True, editable=False, default=generate_unique_uuid)
    date = models.DateField(
        _("date"),
        unique=True,
        error_messages={"unique": "A menu with that date already exists."},
        validators=[MinValueValidator(limit_value=timezone.localdate)],
    )

    class Meta(TimeStampedModel.Meta):
        """Meta options."""

        verbose_name = _("menu")
        verbose_name_plural = _("menus")

    def __str__(self) -> str:
        """Return instance string representation"""
        return f"{self.pk}: {self.date}"

    def get_absolute_url(self):
        """Return url to see instance's detail"""
        return reverse("menus:detail", kwargs={"pk": self.pk})

"""Menus models."""

# Python
import uuid

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.models import SoftDeleteModel, TimeStampedModel


class MenuManager(models.Manager):
    """Menu manager.

    Used to handle uuid creation.
    """

    def create(self, **kwargs):
        """Handle uuid creation."""
        tmp_uuid = str(uuid.uuid4())
        while self.filter(uuid=tmp_uuid).exists():
            tmp_uuid = str(uuid.uuid4())
        kwargs["uuid"] = tmp_uuid
        return super(MenuManager, self).create(**kwargs)


class Menu(TimeStampedModel, SoftDeleteModel):
    """
    Menu model class.

    Extend from TimeStampedModel for default timestamp fields and
    SoftDeleteModel for handling soft delete. Additionally add some
    extra fields.
    """

    objects = MenuManager()

    uuid = models.UUIDField(unique=True, editable=False)
    date = models.DateField(_("date"))

    class Meta:
        """Meta options."""

        verbose_name = _("menu")
        verbose_name_plural = _("menus")

    def __str__(self) -> str:
        """Return instance string representation"""
        return f"{self.pk}: {self.date}"

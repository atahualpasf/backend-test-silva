"""Django models utilities."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.managers import SoftDeleteManager


class TimeStampedModel(models.Model):
    """
    Abstract base class model for provide 'created' and 'modified' timestamp
    fields
    """

    created = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Date time when object was created."),
    )
    modified = models.DateTimeField(
        _("modified at"),
        auto_now=True,
        help_text=_("Date time of last object modification."),
    )

    class Meta:
        """Meta options."""

        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class SoftDeleteModel(models.Model):
    """
    Abstract base class model for provide 'is_deleted' field that
    marks entries that are not going to be used anymore, but are
    kept in database for any reason.
    """

    objects = models.Manager()
    available_objects = SoftDeleteManager()

    is_deleted = models.BooleanField(
        _("soft deleted status"),
        default=False,
        help_text=_("Indicator to know if a object was deleted or not"),
    )

    def soft_delete(self):
        """
        Soft delete object (set its 'is_deleted' field to True).
        """
        self.is_deleted = True
        self.save()

    def soft_restore(self):
        """
        Soft restore object (set its 'is_deleted' field to False).
        """
        self.is_deleted = False
        self.save()

    class Meta:
        """Meta options."""

        abstract = True

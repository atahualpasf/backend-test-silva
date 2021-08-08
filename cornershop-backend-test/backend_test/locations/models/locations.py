"""Locations models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.utils.models import TimeStampedModel


class Location(TimeStampedModel):
    """
    Location model class.

    Extend from TimeStampedModel for default timestamp fields. Additionally
    add some extra fields.
    """

    TYPE_COUNTRY = "country"
    TYPE_ADM_AREA_L1 = "administrative_area_level_1"
    TYPE_ADM_AREA_L2 = "administrative_area_level_2"
    TYPE_LOCALITY = "locality"
    TYPE_NEIGHBORHOOD = "neighborhood"
    TYPE_CHOICES = [
        (TYPE_COUNTRY, _("Country")),
        (TYPE_ADM_AREA_L1, _("Administrative area level 1")),
        (TYPE_ADM_AREA_L2, _("Administrative area level 2")),
        (TYPE_LOCALITY, _("Locality")),
        (TYPE_NEIGHBORHOOD, _("Neighborhood")),
    ]

    location = models.ForeignKey(
        "self",
        verbose_name=_("location"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="locations_location",
        related_query_name="location_location",
    )
    name = models.CharField(_("name"), max_length=85)
    type = models.CharField(_("type"), choices=TYPE_CHOICES, max_length=27)

    class Meta:
        """Meta options."""

        verbose_name = _("location")
        verbose_name_plural = _("locations")
        constraints = [
            models.UniqueConstraint(
                fields=["location", "type", "name"],
                name="location_location_type_name_unique",
            )
        ]

    def __str__(self) -> str:
        """Returning instance string representation"""
        return f"{self.pk}: {self.name}, {self.type}"

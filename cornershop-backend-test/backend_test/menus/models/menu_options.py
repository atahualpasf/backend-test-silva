"""Menu options models."""

# Django
from django.db import models
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.menus.models.meals import Meal
from backend_test.menus.models.menus import Menu
from backend_test.utils.models import TimeStampedModel


class MenuOption(TimeStampedModel):
    """
    Menu option model class.

    Extend from TimeStampedModel for default timestamp fields. Additionally
    add some extra fields.
    """

    menu = models.ForeignKey(
        Menu,
        verbose_name=_("menu"),
        on_delete=models.PROTECT,
        related_name="menu_options",
        related_query_name="menu_option",
    )
    meal = models.ForeignKey(
        Meal,
        verbose_name=_("meal"),
        on_delete=models.PROTECT,
        related_name="menu_options",
        related_query_name="menu_option",
    )
    option = models.PositiveSmallIntegerField(
        _("option"),
        default=BaseDatabaseOperations.integer_field_ranges[
            models.PositiveSmallIntegerField.__name__
        ][1],
        help_text=_("Option number in menu (useful for ordering)."),
    )

    class Meta(TimeStampedModel.Meta):
        """Meta options."""

        verbose_name = _("menu option")
        verbose_name_plural = _("menu options")
        ordering = ["option", "-created"]
        db_table = "menus_menu_option"

    def __str__(self) -> str:
        """Return instance string representation"""
        return f"{self.option}"

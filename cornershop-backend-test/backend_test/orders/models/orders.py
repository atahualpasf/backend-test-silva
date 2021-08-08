"""Orders models."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.menus.models.meals import Meal
from backend_test.menus.models.menus import Menu
from backend_test.users.models.employees import Employee
from backend_test.utils.models import SoftDeleteModel, TimeStampedModel


class Order(TimeStampedModel, SoftDeleteModel):
    """
    Order model class.

    Extend from TimeStampedModel for default timestamp fields and
    SoftDeleteModel for handling soft delete. Additionally add some
    extra fields.
    """

    employee = models.ForeignKey(
        Employee,
        verbose_name=_("employee"),
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name=_("menu"),
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
    )
    meal = models.ForeignKey(
        Meal,
        verbose_name=_("meal"),
        on_delete=models.PROTECT,
        related_name="orders",
        related_query_name="order",
    )
    instructions = models.TextField(
        _("instruccions"),
        blank=True,
        help_text=_("Specify customizations (e.g. no tomatoes in the salad)"),
    )

    class Meta(TimeStampedModel.Meta):
        """Meta options."""

        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self) -> str:
        """Return instance string representation"""
        return f"{self.pk}"

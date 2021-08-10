"""Orders forms."""

# Django
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Backend test
from backend_test.orders.models.orders import Order


# Order form
class OrderForm(forms.ModelForm):
    """Order model form."""

    class Meta:
        """Form settings."""

        model = Order
        fields = "__all__"


# Order form
class OrderUpdateForm(OrderForm):
    """Order model form."""

    class Meta(OrderForm.Meta):
        """Form settings."""

        fields = ["instructions"]

    def clean(self):
        super().clean()
        if not self.instance.menu.is_available():
            raise ValidationError(_("Menu is not available for edition"))

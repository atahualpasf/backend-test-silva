"""Orders forms."""

# Django
from django import forms

# Backend test
from backend_test.orders.models.orders import Order


# Order form
class OrderForm(forms.ModelForm):
    """Order model form."""

    class Meta:
        """Form settings."""

        model = Order
        fields = "__all__"

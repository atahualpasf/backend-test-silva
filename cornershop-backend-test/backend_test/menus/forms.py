"""Menus forms."""

# Django
from django import forms

# Backend test
from backend_test.menus.models.menus import Menu


class MenuForm(forms.ModelForm):
    """Menu model form."""

    class Meta:
        """Form settings."""

        model = Menu
        fields = "__all__"
        widgets = {
            "date": forms.SelectDateWidget(),
        }

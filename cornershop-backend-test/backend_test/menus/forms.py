"""Menus forms."""

# Django
from django import forms

# Backend test
from backend_test.menus.models import Meal, Menu


# Menus form
class MenuForm(forms.ModelForm):
    """Menu model form."""

    class Meta:
        """Form settings."""

        model = Menu
        fields = "__all__"
        widgets = {
            "date": forms.SelectDateWidget(),
        }


# Meals form
class MealForm(forms.ModelForm):
    """Meal model form."""

    class Meta:
        """Form settings."""

        model = Meal
        fields = "__all__"

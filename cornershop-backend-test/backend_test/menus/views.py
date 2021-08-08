"""Menus views."""

# Django
from django.http.response import HttpResponse
from django.views.generic import ListView

# Backend test
from backend_test.menus.models import Menu
from backend_test.utils.mixins import GroupRequiredMixin


def coordinate(request):
    return HttpResponse("Hola coordinate")


def options(request):
    return HttpResponse("Hola options")


class MenusListView(GroupRequiredMixin, ListView):
    """Return all menus."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]
    # Default
    template_name = "menus/list.html"
    model = Menu
    paginate_by = 4
    context_object_name = "menus"

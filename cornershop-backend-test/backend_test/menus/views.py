"""Menus views."""

# Django
from django.http.response import HttpResponse
from django.views.generic import DetailView, ListView

# Backend test
from backend_test.menus.models import Menu, MenuOption
from backend_test.utils.mixins import GroupRequiredMixin


def coordinate(request):
    return HttpResponse("Hola coordinate")


def options(request):
    return HttpResponse("Hola options")


class MenusListView(GroupRequiredMixin, ListView):
    """Return all menus."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # ListView default
    model = Menu
    paginate_by = 4
    context_object_name = "menus"
    template_name = "menus/list.html"


class MenuDetailView(GroupRequiredMixin, DetailView):
    """Return menu detail."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # DetailView default
    model = Menu
    context_object_name = "menu"
    template_name = "menus/detail.html"

    def get_context_data(self, **kwargs):
        """
        Passing menu options of the menu in context data.
        """
        context = super(MenuDetailView, self).get_context_data(**kwargs)
        context["menu_options"] = (
            MenuOption.objects.filter(menu=self.object)
            .select_related("meal")
            .order_by("option")
        )
        return context

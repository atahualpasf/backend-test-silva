"""Menus views."""

# Django
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView

# Backend test
from backend_test.menus.forms import MealForm, MenuForm
from backend_test.menus.models import Meal, Menu, MenuOption
from backend_test.utils.mixins import GroupRequiredMixin


def options(request):
    return HttpResponse("Hola options")


# Menus views
class MenuCreateView(GroupRequiredMixin, CreateView):
    """
    Class to handle menu's creation
    """

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # CreateView default
    model = Menu
    form_class = MenuForm
    template_name = "menus/menus/create.html"


class MenusListView(GroupRequiredMixin, ListView):
    """Return all menus."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # ListView default
    model = Menu
    paginate_by = 2
    context_object_name = "menus"
    template_name = "menus/menus/list.html"


class MenuDetailView(GroupRequiredMixin, DetailView):
    """Return menu detail."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # DetailView default
    model = Menu
    context_object_name = "menu"
    template_name = "menus/menus/detail.html"

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


class MenuUpdateView(GroupRequiredMixin, UpdateView):
    """Class to handle menu's edition."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # UpdateView default
    model = Menu
    form_class = MenuForm
    template_name = "menus/menus/update.html"


class MenuPublicDetailView(DetailView):
    """Return public menu detail."""

    # DetailView default
    model = Menu
    context_object_name = "menu"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    template_name = "menus/menus/public.html"

    def get_context_data(self, **kwargs):
        """
        Passing menu options of the menu in context data.
        """
        context = super(MenuPublicDetailView, self).get_context_data(**kwargs)
        context["menu_options"] = (
            MenuOption.objects.filter(menu=self.object)
            .select_related("meal")
            .order_by("option")
        )
        return context


# Menu options views
def management_menu_options(request, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    MenuOptionInlineFormSet = inlineformset_factory(
        Menu,
        MenuOption,
        fields=(
            "meal",
            "option",
        ),
        can_delete=False,
    )
    if request.method == "POST":
        formset = MenuOptionInlineFormSet(request.POST, request.FILES, instance=menu)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(menu.get_absolute_url())
    else:
        formset = MenuOptionInlineFormSet(instance=menu)
    return render(
        request,
        "menus/menu_options/management.html",
        {"formset": formset, "menu": menu},
    )


# Meals views
class MealCreateView(GroupRequiredMixin, CreateView):
    """
    Class to handle meal's creation
    """

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # CreateView default
    model = Meal
    form_class = MealForm
    template_name = "menus/meals/create.html"


class MealListView(GroupRequiredMixin, ListView):
    """Return all meals."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # ListView default
    model = Meal
    paginate_by = 2
    context_object_name = "meals"
    template_name = "menus/meals/list.html"


class MealDetailView(GroupRequiredMixin, DetailView):
    """Return meal detail."""

    # GroupRequiredMixin
    group_required = ["meal_coordinator"]

    # DetailView default
    model = Meal
    context_object_name = "meal"
    template_name = "menus/meals/detail.html"

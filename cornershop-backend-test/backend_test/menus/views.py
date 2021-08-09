"""Menus views."""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
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
class MenuCreateView(PermissionRequiredMixin, CreateView):
    """
    Class to handle menu's creation
    """

    # PermissionRequiredMixin
    permission_required = ("menus.add_menu",)

    # CreateView default
    model = Menu
    form_class = MenuForm
    template_name = "menus/menus/create.html"


class MenusListView(PermissionRequiredMixin, ListView):
    """Return all menus."""

    # PermissionRequiredMixin
    permission_required = ("menus.view_menu",)

    # ListView default
    model = Menu
    paginate_by = 2
    context_object_name = "menus"
    template_name = "menus/menus/list.html"


class MenuDetailView(PermissionRequiredMixin, DetailView):
    """Return menu detail."""

    # PermissionRequiredMixin
    permission_required = ("menus.view_menu",)

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


class MenuUpdateView(PermissionRequiredMixin, UpdateView):
    """Class to handle menu's edition."""

    # PermissionRequiredMixin
    permission_required = ("menus.change_menu",)

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
@login_required
@permission_required(
    (
        "menus.add_menuoption",
        "menus.change_menuoption",
        "menus.delete_menuoption",
        "menus.view_menuoption",
    ),
    raise_exception=True,
)
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
class MealCreateView(PermissionRequiredMixin, CreateView):
    """
    Class to handle meal's creation
    """

    # PermissionRequiredMixin
    permission_required = ("menus.add_meal",)

    # CreateView default
    model = Meal
    form_class = MealForm
    template_name = "menus/meals/create.html"


class MealListView(PermissionRequiredMixin, ListView):
    """Return all meals."""

    # PermissionRequiredMixin
    permission_required = ("menus.view_meal",)

    # ListView default
    model = Meal
    paginate_by = 2
    context_object_name = "meals"
    template_name = "menus/meals/list.html"


class MealDetailView(PermissionRequiredMixin, DetailView):
    """Return meal detail."""

    # PermissionRequiredMixin
    permission_required = ("menus.view_meal",)

    # DetailView default
    model = Meal
    context_object_name = "meal"
    template_name = "menus/meals/detail.html"

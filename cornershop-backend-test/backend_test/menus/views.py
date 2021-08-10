"""Menus views."""
# Python
import json

# Django
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.sites.models import Site
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.encoding import force_str
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# Backend test
from backend_test.menus.forms import MealForm, MenuForm
from backend_test.menus.models import Meal, Menu, MenuOption
from backend_test.menus.tasks import send_menu_public_url_task
from backend_test.orders.models.orders import Order
from backend_test.users.models import Employee


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

    # OPTIMIZE: Check again to simplify order generation
    def get_context_data(self, **kwargs):
        """
        Passing menu options of the menu in context data.
        """
        context = super(MenuPublicDetailView, self).get_context_data(**kwargs)

        # Load menu options
        context["menu_options"] = (
            MenuOption.objects.filter(menu=self.object)
            .select_related("meal")
            .order_by("option")
        )

        # Load employee if exists
        try:
            employee = (
                self.request.user.employees.get()
                if self.request.user.is_authenticated
                else None
            )
        except Employee.DoesNotExist:
            employee = None
        context["employee"] = employee

        # Verify if already generated order
        order = (
            Order.objects.filter(
                employee_id=employee.pk, menu_id=self.object.pk
            ).first()
            if employee
            else None
        )
        context["order"] = order

        # Verify valid user
        context["is_valid_user"] = not self.request.user.is_authenticated or employee
        return context


@require_POST
@permission_required("menus.send_slack_reminder")
def send_slack_reminder(request):
    menu_id = request.POST.get("menu", None)
    menu = Menu.objects.filter(pk=menu_id).first() if menu_id else None

    # Check if menu exists
    if not menu:
        return render(
            request,
            "handler.html",
            {"msg": "An error has occurred processing your request."},
        )

    # Check if menu is available
    if not menu.is_available():
        return render(
            request,
            "handler.html",
            {"msg": "Menu is unavailable."},
        )

    menu_options = (
        MenuOption.objects.filter(menu_id=menu.pk)
        .select_related("meal")
        .order_by("option")
    )

    # Check if menu has menu options
    if not menu_options:
        return render(
            request,
            "handler.html",
            {"msg": "Can't sent reminder if the menu has not options."},
        )

    # Check if site exists
    site = Site.objects.filter(pk=settings.SITE_ID).first()
    if not site:
        return render(
            request,
            "handler.html",
            {"msg": "Can't sent reminder if the menu has not options."},
        )

    template_params = {
        "action_url": f"https://{site}"
        + reverse("menus:public", kwargs={"uuid": menu.uuid}),
        "menu_options": menu_options,
    }
    data = json.loads(
        force_str(
            render_to_string(
                "menus/menus/slack/today_reminder.json",
                template_params,
            ).strip()
        )
    )
    text = force_str(
        render_to_string(
            "menus/menus/slack/today_reminder_text.html",
            template_params,
        ).strip()
    )
    send_menu_public_url_task.delay(data, text)

    return render(
        request,
        "handler.html",
        {"msg": "Reminder has sent successfully", "success": True},
    )


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
    """
    View function that allow create and update multiple menu options.
    """
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
        formset = MenuOptionInlineFormSet(request.POST, instance=menu)
        if formset.is_valid():
            formset.save()
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

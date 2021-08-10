"""Orders views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from backend_test.menus.models.menus import Menu

# Backend test
from backend_test.orders.forms import OrderForm, OrderUpdateForm
from backend_test.orders.models.orders import Order
from backend_test.users.models.employees import Employee


class GenerateOrderView(View):
    """Class to handle order generation request."""

    form_class = OrderForm

    # OPTIMIZE: This method need to be refactor. Code smell and is dont follow DRY
    def post(self, request, *args, **kwargs):
        """
        Post view function to handle order generation.
        """
        # Get menu for redirection
        menu_pk = request.POST.get("menu", None)
        menu = Menu.objects.filter(pk=menu_pk).first() if menu_pk else None

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                "{}?next={}".format(
                    reverse("users:login"),
                    reverse("menus:public", kwargs={"uuid": menu.uuid}) if menu else "",
                )
            )

        # Validate if not menu
        if not menu:
            return render(
                request,
                "orders/error.html",
                {"msg": "An error has occurred processing your request."},
            )

        # Verify if menu is available
        if not menu.is_available:
            return render(
                request,
                "orders/error.html",
                {"msg": "This menu is unavailable at this time.", "menu": menu},
            )

        # Check if the user is an employee
        try:
            employee = (
                self.request.user.employees.get()
                if self.request.user.is_authenticated
                else None
            )
        except Employee.DoesNotExist:
            employee = None
        if not employee:
            return render(
                request,
                "orders/error.html",
                {"msg": "You have to be a Cornershop employee to order.", "menu": menu},
            )
        if str(employee.pk) != request.POST.get("employee", None):
            return HttpResponseRedirect(reverse("users:logout"))

        # Verify if employee already has an order
        order = (
            Order.objects.filter(
                employee_id=request.POST.get("order", None), menu_id=menu.pk
            ).first()
            if employee
            else None
        )
        if order:
            return render(
                request,
                "orders/error.html",
                {"msg": "You already have an order with this menu", "menu": menu},
            )

        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(
                request,
                "orders/error.html",
                {"msg": "An error has occurred processing your request.", "menu": menu},
            )

        order = form.save()
        return redirect(reverse("orders:update", kwargs={"pk": order.pk}))


class OrderDetailView(PermissionRequiredMixin, DetailView):
    """Return order detail."""

    # PermissionRequiredMixin
    permission_required = ("orders.view_order",)

    # DetailView default
    model = Order
    context_object_name = "order"
    template_name = "orders/detail.html"

    def has_permission(self) -> bool:
        """
        Allowing if the employee is the order's owner. If not is the owner
        check the permissions in permission_required.
        """
        order = self.get_object()
        try:
            employee = (
                self.request.user.employees.get()
                if self.request.user.is_authenticated
                else None
            )
        except Employee.DoesNotExist:
            employee = None
        if employee and order.employee.pk == employee.pk:
            return True
        return super().has_permission()


class OrderOwnListView(LoginRequiredMixin, ListView):
    """Return orders filter by owner."""

    # ListView default
    model = Order
    paginate_by = 2
    context_object_name = "orders"
    template_name = "orders/list.html"

    def get_queryset(self):
        """
        Getting only the orders by owner.
        """
        return (
            super()
            .get_queryset()
            .select_related("employee__user")
            .select_related("meal")
            .select_related("menu")
            .filter(employee__user_id=self.request.user.pk)
        )


class OrderListView(OrderOwnListView):
    """Return all orders."""

    # PermissionRequiredMixin
    permission_required = ("orders.view_order",)

    def get_queryset(self):
        """
        Getting all orders without filter
        """
        return (
            Order.objects.select_related("employee__user")
            .select_related("meal")
            .select_related("menu")
            .all()
        )


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    """Class to handle orders's edition."""

    # PermissionRequiredMixin
    permission_required = ("orders.change_order",)

    # UpdateView default
    model = Order
    form_class = OrderUpdateForm
    template_name = "orders/update.html"

    def has_permission(self) -> bool:
        """
        Allowing if the employee is the order's owner. If not is the owner
        check the permissions in permission_required.
        """
        order = self.get_object()
        if order.employee.user.pk == self.request.user.pk:
            return True
        return super().has_permission()

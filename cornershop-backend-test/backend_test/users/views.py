"""Users views."""

# Django
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse


@login_required
def index(request):
    """Redirecting to default view for each type of user (employees or Nora)"""
    group = [group.name for group in request.user.groups.filter(user=request.user)]

    if "meal_coordinator" in group:
        return HttpResponseRedirect(reverse("menus:index"))

    return HttpResponseRedirect(reverse("menus:options"))


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = "users/login.html"


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = "users/logged_out.html"

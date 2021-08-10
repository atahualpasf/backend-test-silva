"""Users views."""

# Django
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "users/index.html")


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = "users/login.html"


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = "users/logged_out.html"

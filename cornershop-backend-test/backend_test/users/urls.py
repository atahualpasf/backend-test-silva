"""Users urls."""

# Django
from django.urls import path

# Backend test
from backend_test.users import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="login", view=views.LoginView.as_view(), name="login"),
    path(route="logout", view=views.LogoutView.as_view(), name="logout"),
]

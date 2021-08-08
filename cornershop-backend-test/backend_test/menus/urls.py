"""Menus urls."""

# Django
from django.urls import path

# Backend test
from backend_test.menus import views

urlpatterns = [
    path(route="", view=views.MenusListView.as_view(), name="index"),
    path(route="<int:pk>", view=views.MenuDetailView.as_view(), name="index"),
    path(route="coordinate", view=views.coordinate, name="coordinate"),
    path(route="options", view=views.options, name="options"),
]

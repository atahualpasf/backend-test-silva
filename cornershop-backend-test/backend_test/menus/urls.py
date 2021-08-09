"""Menus urls."""

# Django
from django.urls import path

# Backend test
from backend_test.menus import views

urlpatterns = [
    path(route="", view=views.MenusListView.as_view(), name="index"),
    path(route="create", view=views.MenuCreateView.as_view(), name="create"),
    path(route="<int:pk>/update", view=views.MenuUpdateView.as_view(), name="update"),
    path(route="<int:pk>", view=views.MenuDetailView.as_view(), name="detail"),
    path(route="options", view=views.options, name="options"),
]

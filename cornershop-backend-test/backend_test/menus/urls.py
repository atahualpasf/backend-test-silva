"""Menus urls."""

# Django
from django.urls import include, path

# Backend test
from backend_test.menus import views

menu_options_patterns = [
    path(route="management", view=views.management_menu_options, name="management"),
]

meals_patterns = [
    path(route="", view=views.MealListView.as_view(), name="index"),
    path(route="create", view=views.MealCreateView.as_view(), name="create"),
    path(route="<int:pk>", view=views.MealDetailView.as_view(), name="detail"),
]

urlpatterns = [
    path(route="", view=views.MenusListView.as_view(), name="index"),
    path(route="create", view=views.MenuCreateView.as_view(), name="create"),
    path(route="<int:pk>/update", view=views.MenuUpdateView.as_view(), name="update"),
    path(route="<int:pk>", view=views.MenuDetailView.as_view(), name="detail"),
    path(route="<uuid:uuid>", view=views.MenuPublicDetailView.as_view(), name="public"),
    path(
        "<int:menu_id>/options/",
        include((menu_options_patterns, "options"), namespace="options"),
    ),
]

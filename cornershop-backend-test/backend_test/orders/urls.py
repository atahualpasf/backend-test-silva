"""Orders urls."""

# Django
from django.urls import path

# Backend test
from backend_test.orders import views

urlpatterns = [
    path(route="", view=views.OrderListView.as_view(), name="index"),
    path(route="mine", view=views.OrderOwnListView.as_view(), name="mine-list"),
    path(route="generate", view=views.GenerateOrderView.as_view(), name="generate"),
    path(route="<int:pk>/update", view=views.OrderUpdateView.as_view(), name="update"),
    path(route="<int:pk>", view=views.OrderDetailView.as_view(), name="detail"),
]

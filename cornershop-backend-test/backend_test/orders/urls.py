"""Orders urls."""

# Django
from django.urls import path

# Backend test
from backend_test.orders import views

urlpatterns = [
    path(route="generate", view=views.GenerateOrderView.as_view(), name="generate"),
    path(route="<int:pk>", view=views.OrderDetailView.as_view(), name="detail"),
]

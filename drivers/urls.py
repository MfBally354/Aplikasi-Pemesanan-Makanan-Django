from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path("dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path("orders/available/", views.driver_available_orders, name="driver_available_orders"),
    path("take-order/<int:order_id>/", views.take_order, name="take_order"),
    path("update-status/<int:order_id>/", views.update_status, name="update_status"),
    path("history/", views.driver_history, name="driver_history"),
]

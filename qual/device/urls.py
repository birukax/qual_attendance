from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "device"

urlpatterns = [
    path("devices", views.devices, name="devices"),
    path("create_device", views.create_device, name="create_device"),
    path("devices/<int:id>", views.device_detail, name="device_detail"),
    path("devices/<int:id>/restart/", views.restart_device, name="restart_device"),
    path("devices/<int:id>/users", views.device_users, name="device_users"),
    path("sync_users/<int:id>", views.sync_users, name="sync_users"),
    path("sync_time/<int:id>", views.sync_time, name="sync_time"),
    path("add_employee/<int:id>", views.add_employee, name="add_employee"),
]

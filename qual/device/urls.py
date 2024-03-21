from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "device"

urlpatterns = [
    path("devices", views.devices, name="devices"),
    path("create_device", views.create_device, name="create_device"),
    path("devices/<int:id>", views.device_detail, name="device_detail"),
    path("sync_users/<int:id>", views.sync_users, name="sync_users"),
    path("add_employee/<int:id>", views.add_employee, name="add_employee"),
]

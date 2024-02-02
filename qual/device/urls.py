from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "device"

urlpatterns = [
    path("devices", views.devices, name="devices"),
    path("devices/<int:id>", views.device_detail, name="device_detail"),
    path("create_device", views.create_device, name="create_device"),
    
]
from django.contrib import admin
from .models import Device, DeviceUser


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "ip", "port"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 15


@admin.register(DeviceUser)
class DeviceUserAdmin(admin.ModelAdmin):
    list_display = ["uid", "name", "user_id", "device"]
    list_per_page = 15
    list_filter = ["device"]
    search_fields = ["name", "user_id"]

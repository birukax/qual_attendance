from django.contrib import admin
from .models import *


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "leave_type",
        "half_day",
        "active",
        "start_date",
        "end_date",
        "approved",
        "rejected",
    ]
    search_fields = ["employee__name"]
    list_per_page = 15


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "description",
        "maximum_days",
        "paid",
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 15

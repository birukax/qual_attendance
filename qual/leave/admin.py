from django.contrib import admin
from .models import *


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "leave_type",
        "half_day",
        "saturday_half",
        "active",
        "start_date",
        "end_date",
        "approved",
        "rejected",
    ]
    search_fields = ["employee__name"]
    list_filter = ["leave_type", "approved", "rejected", "half_day", "saturday_half"]
    list_per_page = 50


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "description",
        "maximum_days",
        "paid",
        "exclude_rest_days",
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["paid", "exclude_rest_days"]
    list_per_page = 50

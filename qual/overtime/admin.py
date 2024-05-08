from django.contrib import admin
from .models import *


@admin.register(OvertimeType)
class OvertimeTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "day_span",
        "pay_item_code",
        "start_time",
        "end_time",
    ]
    list_per_page = 15


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "start_date",
        "end_date",
        "approved",
        "start_time",
        "end_time",
        "paid",
    ]
    list_per_page = 15


@admin.register(Ot)
class OtAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "start_date",
        "end_date",
        "start_time",
        "end_time",
        "units_worked",
    ]


@admin.register(Day)
class Day(admin.ModelAdmin):
    list_display = [
        "no",
        "name",
    ]

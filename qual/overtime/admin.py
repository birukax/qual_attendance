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
        "worked_hours",
        "start_time_expected",
        "start_time_expected",
        "end_time_actual",
        "end_time_actual",
    ]
    list_per_page = 15


@admin.register(Ot)
class OtAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "date",
        "units_worked",
        "start_time",
        "end_time",
    ]


@admin.register(Day)
class Day(admin.ModelAdmin):
    list_display = [
        "no",
        "name",
    ]

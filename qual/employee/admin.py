from django.contrib import admin

from .models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "employee_id",
        "name",
        "department",
        "shift",
        "employment_date",
        "status",
    ]
    search_fields = [
        "name",
    ]
    list_per_page = 15


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]


# @admin.register(Salary)
# class SalaryAdmin(admin.ModelAdmin):
#     list_display = ["employee", "salary", "effective_date", "end_date"]
#     search_fields = ["employee__name"]
#     list_per_page = 15

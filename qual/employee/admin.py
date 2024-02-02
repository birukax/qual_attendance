from django.contrib import admin

from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id','name', 'shift', 'pattern', 'last_updated' ]
    search_fields = ['name',]

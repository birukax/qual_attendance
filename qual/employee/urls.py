from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path("employees", views.employees, name="employees"),
    path("departments", views.departments, name="departments"),
    path("sync_employee", views.sync_employee, name="sync_employee"),
    path("employees/<int:id>", views.employee_detail, name="employee_detail"),
    path(
        "employees/<int:id>/attendances",
        views.employee_attendances,
        name="employee_attendances",
    ),
    path("employees/<int:id>/leaves", views.employee_leaves, name="employee_leaves"),
    path(
        "employees/<int:id>/overtimes",
        views.employee_overtimes,
        name="employee_overtimes",
    ),
]

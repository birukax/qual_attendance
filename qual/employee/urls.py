from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path("employees", views.employees, name="employees"),
    path("departments", views.departments, name="departments"),
    path("sync_employee", views.sync_employee, name="sync_employee"),
    # path("update_salary", views.update_salary, name="update_salary"),
    # path("sync_department", views.sync_department, name="sync_department"),
    path("employees/<int:id>", views.employee_detail, name="employee_detail"),
]

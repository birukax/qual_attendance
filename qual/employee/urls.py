from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name = "employee"

urlpatterns = [
    path("employees", views.employees, name="employees"),
    path("sync_employee", views.sync_employee, name="sync_employee"),
    path("employees/<int:id>", views.employee_detail, name="employee_detail"),
    
]
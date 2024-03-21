from django.urls import path, reverse
from . import views
from django.contrib.auth import views as auth_views

app_name = "shift"

urlpatterns = [
    path("change_shift/<int:id>", views.change_shift, name="change_shift"),
    path("shifts", views.shifts, name="shifts"),
    path("select_employees", views.select_employees, name="select_employees"),
    path("set_employees", views.set_employees, name="set_employees"),
    path("assign_employees", views.assign_employees, name="assign_employees"),
    path("shifts/<int:id>", views.shift_detail, name="shift_detail"),
    path("create_shift", views.create_shift, name="create_shift"),
    path("edit_pattern/<int:id>", views.edit_pattern, name="edit_pattern"),
    path("edit_shift/<int:id>", views.edit_shift, name="edit_shift"),
]

from django.urls import path
from . import views

app_name = "overtime"

urlpatterns = [
    path("overtimes", views.overtimes, name="overtimes"),
    path("overtime_detail/<int:id>", views.overtime_detail, name="overtime_detail"),
    path("approve_overtime/<int:id>", views.approve_overtime, name="approve_overtime"),
    path(
        "calculate_overtime/<int:id>",
        views.calculate_overtime,
        name="calculate_overtime",
    ),
    path("overtime_types", views.overtime_types, name="overtime_types"),
    path(
        "edit_overtime_type/<int:id>",
        views.edit_overtime_type,
        name="edit_overtime_type",
    ),
    path("create_overtime", views.create_overtime, name="create_overtime"),
    path(
        "create_overtime_type", views.create_overtime_type, name="create_overtime_type"
    ),
    path(
        "overtime_type_detail/<int:id>",
        views.overtime_type_detail,
        name="overtime_type_detail",
    ),
]

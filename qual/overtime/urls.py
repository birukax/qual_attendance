from django.urls import path
from . import views

app_name = "overtime"

urlpatterns = [
    path("overtimes", views.overtimes, name="overtimes"),
    path("download_overtime", views.download_overtime, name="download_overtime"),
    path("overtime_detail/<int:id>", views.overtime_detail, name="overtime_detail"),
    path(
        "calculate_ots",
        views.calculate_ots,
        name="calculate_ots",
    ),
    path("post_overtime", views.post_overtime, name="post_overtime"),
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
    path("ots", views.ots, name="ots"),
]

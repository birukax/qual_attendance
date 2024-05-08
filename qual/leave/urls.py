from django.urls import path
from . import views

app_name = "leave"

urlpatterns = [
    path("leaves/", views.leave_list, name="leaves"),
    path("annual_leaves/", views.annual_leave_list, name="annual_leaves"),
    path("create/", views.create_leave, name="create_leave"),
    path("calculate/", views.calculate_leave_balance, name="calculate_leave_balance"),
    path(
        "annual_leave/download",
        views.download_annual_leave,
        name="download_annual_leave",
    ),
    # path("aprove_leave/<int:id>/", views.approve_leave, name="approve_leave"),
    path("leave_type/create", views.create_leave_type, name="create_leave_type"),
    path("leave_types/", views.leave_type_list, name="leave_types"),
    path("leave_types/edit/<int:id>/", views.edit_leave_type, name="edit_leave_type"),
    path("leave_types/<int:id>/", views.leave_type_detail, name="leave_type_detail"),
    path("<int:id>/", views.leave_detail, name="leave_detail"),
]

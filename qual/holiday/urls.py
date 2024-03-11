from django.urls import path
from . import views

app_name = "holiday"

urlpatterns = [
    path(
        "holidays",
        views.holidays,
        name="holidays",
    ),
    path("holiday/<int:id>", views.holiday_detail, name="holiday_detail"),
    path("create_holiday", views.create_holiday, name="create_holiday"),
    path("approve_holiday/<int:id>", views.approve_holiday, name="approve_holiday"),
]

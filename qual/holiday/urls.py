from django.urls import path
from . import views

app_name = "holiday"

urlpatterns = [
    path(
        "holidays",
        views.holidays,
        name="holidays",
    ),
    path("create_holiday", views.create_holiday, name="create_holiday"),
    path("approve_holiday/<int:id>", views.approve_holiday, name="approve_holiday"),
]

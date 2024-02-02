from django.urls import path, reverse
from .import views
from django.contrib.auth import views as auth_views

app_name = "shift"

urlpatterns = [
    path("change_shift/<int:id>", views.change_shift, name="change_shift"),
    path("change_pattern/<int:id>", views.change_pattern, name="change_pattern"),
    path("shifts", views.shifts, name="shifts"),
    path("shifts/<int:id>", views.shift_detail, name="shift_detail"),
    path("create_shift", views.create_shift, name="create_shift"),
    path("edit_pattern/<int:id>", views.edit_pattern, name="edit_pattern"),
    path("edit_shift/<int:id>", views.edit_shift, name="edit_shift")
    
    
]
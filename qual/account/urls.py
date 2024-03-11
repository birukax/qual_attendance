from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "account"

urlpatterns = [
    path("users/", views.users, name="users"),
    path("user/create", views.create_user, name="create_user"),
    path("user/edit/<int:id>/", views.edit_user, name="edit_user"),
    path("profile/edit/<int:id>/", views.edit_profile, name="edit_profile"),
    path("profile/<int:id>/", views.profile_detail, name="profile_detail"),
    path("user/<int:id>/", views.user_detail, name="user_detail"),
    path("edit/<int:id>", views.edit, name="edit"),
]

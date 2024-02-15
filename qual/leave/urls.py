from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('', views.leave_list, name='leaves'),
    path('<int:id>/', views.leave_detail, name='leave_detail'),
    path('create/', views.create_leave, name='create_leave'),
    path('leave_type/create', views.create_leave_type, name='create_leave_type'),
    path("leave_types/", views.leave_type_list, name="leave_types"),
    path("leave_types/edit/<int:id>/", views.edit_leave_type, name="edit_leave_type"),
    path("leave_types/<int:id>/", views.leave_type_detail, name="leave_type_detail"),
]
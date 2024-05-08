"""
URL configuration for qual project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    path("select", include("django_select2.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="user/profile/password/change.html"
        ),
        name="password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="user/profile/password/done.html"
        ),
        name="password_change_done",
    ),
    path("admin/", admin.site.urls),
    path("", include("attendance.urls")),
    path("users/", include("account.urls")),
    path("approval/", include("approval.urls")),
    path("devices/", include("device.urls")),
    path("shifts/", include("shift.urls")),
    path("employees/", include("employee.urls")),
    path("leaves/", include("leave.urls")),
    path("holidays/", include("holiday.urls")),
    path("overtime/", include("overtime.urls")),
    re_path(r"session_security/", include("session_security.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

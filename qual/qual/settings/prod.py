from .base import *

ADMIN = [("admin", "admin@email.com")]
ALLOWED_HOSTS = ["*"]
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "host.docker.internal",
        "NAME": "qual",
        "USER": "admin",
        "PASSWORD": "password",
        "PORT": 5432,
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

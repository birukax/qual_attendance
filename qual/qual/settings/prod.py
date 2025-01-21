from .base import *
from decouple import config

ADMIN = [("admin", "admin@email.com")]
SECRET_KEY = config("SECRET_KEY")
# DEBUG = False
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "NAME": "qual",
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "PORT": 5432,
    }
}

ROOT_URLCONF = "qual.qual.urls"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

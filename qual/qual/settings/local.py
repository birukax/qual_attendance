from .base import *
from decouple import config


DEBUG = True
ALLOWED_HOSTS = ["*"]
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

SECURE_SSL_REDIRECT = False

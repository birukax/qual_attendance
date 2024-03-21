from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "NAME": "qual",
        "USER": "admin",
        "PASSWORD": "password",
        "PORT": 5432,
    }
}

SECURE_SSL_REDIRECT = False

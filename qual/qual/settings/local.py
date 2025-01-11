from .base import *
from decouple import config

SECRET_KEY = "django-insecure-(4x*c^lqncc)!e4vp4qb6x06y7ojqh@z*dhxc)l45mf8o%!jqb"

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

SECURE_SSL_REDIRECT = False

from .base import *

ROOT_URLCONF = "qual.urls"

debug = True
SECRET_KEY = "django-insecure-(4x*c^lqncc)!e4vp4qb6x06y7ojqh@z*dhxc)l45mf8o%!jqb"

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "172.16.18.23",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "PORT": 5432,
    }
}

SECURE_SSL_REDIRECT = False

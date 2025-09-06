from .base import *

ROOT_URLCONF = "qual.urls"

debug = True
SECRET_KEY = "django-insecure-(4x*c^lqncc)!e4vp4qb6x06y7ojqh@z*dhxc)l45mf8o%!jqb"

DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config("DB_HOST"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "PORT": 5432,
    }
}

SECURE_SSL_REDIRECT = False


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": config("CACHE_LOCATION"),  # Path to the cache directory
    }
}

SELECT2_CACHE_BACKEND = "default"

from .base import *

ADMIN = [("admin", "admin@email.com")]
SECRET_KEY = config("SECRET_KEY")
# DEBUG = False
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

ROOT_URLCONF = "qual.qual.urls"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": config("CACHE_LOCATION"),  # Path to the cache directory
    }
}

SELECT2_CACHE_BACKEND = "default"

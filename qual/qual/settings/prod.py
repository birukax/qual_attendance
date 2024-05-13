from .base import *
from decouple import config

ADMIN = [("admin", "admin@email.com")]
ALLOWED_HOSTS = ["*"]
DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "host.docker.internal",
        "NAME": "qual",
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "PORT": 5432,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    },
    "select2": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    },
}

SELECT2_CACHE_BACKEND = "select2"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

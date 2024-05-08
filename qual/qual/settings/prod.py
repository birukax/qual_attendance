from .base import *

ADMIN = [("admin", "admin@email.com")]
ALLOWED_HOSTS = ["*"]
DEBUG = False
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

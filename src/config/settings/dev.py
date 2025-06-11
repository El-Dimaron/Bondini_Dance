import os

from config.settings.base import *  # NOQA:F403

SECRET_KEY = "django-insecure-&=nand4!!4ul2+8od3u3zws1+je0al^_+-=5jf25^8b_tn*-f*"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ["django_extensions"]  # NOQA: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA:F405
    }
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "common/static"]  # NOQA:F405

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # NOQA:F405

INTERNAL_IPS = [
    "127.0.0.1",
]

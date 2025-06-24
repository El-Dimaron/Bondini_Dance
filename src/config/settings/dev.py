import os

import mongoengine
from dotenv import load_dotenv

from config.settings.base import *  # NOQA:F403

SECRET_KEY = "django-insecure-&=nand4!!4ul2+8od3u3zws1+je0al^_+-=5jf25^8b_tn*-f*"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ["django_extensions"]  # NOQA: F405

load_dotenv()

mongoengine.connect(
    host=os.environ.get("DJANGO_MONGO_CONNECTION"),
)

IS_DOCKER = os.environ.get("DOCKER", "0") == "1"

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        },
    }
else:
    DATABASES = {
        "default_sqlite": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # NOQA:F405
        },
        "default_local": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "bd_db",
            "USER": "El-Dimaron",
            "PASSWORD": "admin",
            "HOST": "localhost",
            "PORT": 5433,
        },
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": "postgres" if IS_DOCKER else "localhost",
            "PORT": os.environ.get("POSTGRES_PORT"),
        },
    }

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # NOQA:F405

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # NOQA:F405

INTERNAL_IPS = [
    "127.0.0.1",
]

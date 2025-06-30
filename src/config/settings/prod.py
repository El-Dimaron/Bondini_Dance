import os

from config.settings.base import *  # NOQA:F403

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["*"]

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
            "PORT": "5432" if IS_DOCKER else os.environ.get("POSTGRES_PORT"),
        },
    }

STATIC_ROOT = BASE_DIR / "static/"  # NOQA: F405
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media/"  # NOQA: F405
MEDIA_URL = "/media/"

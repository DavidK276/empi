"""
Django settings for empi_server project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os

from pathlib import Path

import sentry_sdk

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bn7i4a#e6&%@jrs!y5%n(et7c!d*f1!%e7i7@9h$p4v)jl&$$^"

secret_key_var = os.environ.get("DJANGO_SECRET_KEY", "")
if secret_key_var:
    SECRET_KEY = secret_key_var.strip()
else:
    print(
        "\033[93m"
        + "Environment variable DJANGO_SECRET_KEY is not set. SECRET_KEY will use an insecure value."
        + "\033[0m"
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "0") == "1"
if DEBUG:
    print("\033[93m" + "Django debug is enabled. Remember to not run with debug turned on in production." + "\033[0m")

ALLOWED_HOSTS = []
hosts = os.environ.get("ALLOWED_HOSTS", "").strip('"').strip("'")
if hosts:
    ALLOWED_HOSTS = hosts.split(",")
if os.environ.get("EMPI_DOCKER", ""):
    ALLOWED_HOSTS += ["api"]

csrf_trusted_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip('"').strip("'")

if csrf_trusted_origins:
    CSRF_TRUSTED_ORIGINS = csrf_trusted_origins.split(",")
else:
    CSRF_TRUSTED_ORIGINS = []

BASE_URI = (os.environ.get("BASE_URI", "").strip("/") + "/").lstrip("/")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = ("http://localhost:5173",)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "knox",
    "users",
    "research",
    "emails",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "empi_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "empi_server.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if os.environ.get("EMPI_DOCKER", ""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "postgres"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
            "HOST": os.environ.get("DB_HOST", "db"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "knox.auth.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

REST_KNOX = {"USER_SERIALIZER": "users.serializers.UserSerializer", "AUTH_HEADER_PREFIX": "Bearer"}

SPECTACULAR_SETTINGS = {
    "TITLE": "Empi API",
    "DESCRIPTION": "The backend API of Empi",
    "VERSION": "0.2.0",
    "SERVE_INCLUDE_SCHEMA": True,
    "SERVERS": [{"url": "http://localhost:8000"}],
}

sentry_sdk_dsn = os.environ.get("SENTRY_SDK_DSN", "").strip('"').strip("'")
if sentry_sdk_dsn:
    sentry_sdk.init(
        dsn=sentry_sdk_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=0.01,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=0.01,
        send_default_pii=True,
        auto_session_tracking=False,
    )

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "sk-sk"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = BASE_URI + "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR.parent / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.EmpiUser"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMPI_PUBLIC_URL = (os.environ.get("WEB_URL") or "http://localhost:5173").strip("/")

EMPI_FROM_EMAIL = os.environ.get("FROM_EMAIL") or "noreply@example.com"
EMPI_REPLY_TO_EMAILS = (os.environ.get("REPLY_TO_EMAILS") or "admin@example.com").strip('"').strip("'").split(",")

"""
Django settings for minesweeper_api project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import ipaddress
import os
from copy import deepcopy

import django_heroku
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"


# Application definition

INSTALLED_APPS = [
    # Custom apps.
    "minesweeper_api_user.apps.MinesweeperApiUserConfig",
    "ms_game.apps.MsGameConfig",
    # Third-party apps
    "rest_framework",
    "corsheaders",
    # Base django apps.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Development apps.
    "django_extensions",
    "sslserver",
    "drf_yasg",
    # Keep last so any app can override templates.
    "django.forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "minesweeper_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "minesweeper_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {"default": None}

if "DATABASE_URL" not in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DATABASE_NAME"],
            "USER": os.environ["DATABASE_USER"],
            "PASSWORD": os.environ["DATABASE_PASSWORD"],
            "HOST": os.environ["DATABASE_HOST"],
            "PORT": os.environ["DATABASE_PORT"],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "mineswepper_ui", "dist"),
]
# Ensure directories exist.
# Django only creates "static". ANy other will cause an error.
for directory in STATICFILES_DIRS:
    os.makedirs(directory, exist_ok=True)


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Email
# https://docs.djangoproject.com/en/dev/topics/email/

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == "True"

if "DEFAULT_FROM_EMAIL" in os.environ:
    DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]

if "SERVER_EMAIL" in os.environ:
    SERVER_EMAIL = os.environ["SERVER_EMAIL"]

MANAGERS = [("", email.strip()) for email in os.getenv("MANAGERS", "").split()]
ADMINS = [("", email.strip()) for email in os.getenv("ADMINS", "").split()]


# Custom User model
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

AUTH_USER_MODEL = "minesweeper_api_user.User"


# Authentication backends model
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#specifying-authentication-backends

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "minesweeper_api_user.auth.SettingsBackend",
]
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


# https://www.fomfus.com/articles/how-to-use-ip-ranges-for-django-s-internal_ips-setting
class IpNetworks:
    """
    A Class that contains a list of IPvXNetwork objects.

    Credits to https://djangosnippets.org/snippets/1862/
    """

    networks = []

    def __init__(self, addresses):
        """Create a new IpNetwork object for each address provided."""
        for address in addresses:
            self.networks.append(ipaddress.ip_network(address))

    def __contains__(self, address):
        """Check if the given address is contained in any of our Networks."""
        for network in self.networks:
            if ipaddress.ip_address(address) in network:
                return True
        return False


if os.environ.get("INTERNAL_ADDRESSES"):
    INTERNAL_IPS = IpNetworks(os.environ["INTERNAL_ADDRESSES"].split(" "))


# SSL Settings.
# Trust Proxy header and redirect to SSL.
# https://docs.djangoproject.com/en/dev/ref/middleware/#django.middleware.security.SecurityMiddleware
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Allowed hosts
# https://docs.djangoproject.com/en/dev/topics/security/#host-headers-virtual-hosting
if os.environ.get("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(" ")


# Django Rest Framework
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "ms_game.authentication.EmailAuth",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}


# CORS
# https://github.com/adamchainz/django-cors-headers
CORS_ORIGIN_WHITELIST = [
    url.strip() for url in os.getenv("CORS_ORIGIN_WHITELIST", "").split()
]
CORS_ALLOW_CREDENTIALS = True


# https://docs.djangoproject.com/en/dev/topics/logging/#default-logging-configuration
# Colorize output, and make it more verbose.
LOGGING = deepcopy(DEFAULT_LOGGING)
LOGGING["formatters"]["logger"] = {
    "format": (
        "\033[35m%(asctime)s\033[0m \033[31m[%(levelname)s]\033[0m "
        "\033[34m[%(name)s]\033[0m %(message)s"
    )
}
LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["handlers"]["console"]["formatter"] = "logger"
LOGGING["loggers"][""] = deepcopy(LOGGING["loggers"]["django"])
LOGGING["loggers"]["django"]["level"] = os.environ.get("DJANGO_LOGGING_LEVEL", "INFO")
LOGGING["loggers"]["django"]["propagate"] = False
LOGGING["loggers"][""]["level"] = os.environ.get("ROOT_LOGGING_LEVEL", "INFO")


# Activate Django-Heroku.
# Useful even when not using Heroku.
django_heroku.settings(
    locals(), allowed_hosts="ALLOWED_HOSTS" not in locals(), logging=False
)

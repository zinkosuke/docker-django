import os

from django.utils.translation import gettext_lazy as _

"""Base.
"""
BASE_DIR = os.environ["DJANGO_HOME"]
WSGI_PPLICATION = "settings.wsgi.application"
ROOT_URLCONF = "settings.urls"

"""Auth.
"""
AUTH_USER_MODEL = "accounts.User"

"""Static files.
"""
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

"""Locale.
"""
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
LANGUAGE_CODE = "ja"
LANGUAGES = [("ja", _("Japanese"))]
USE_I18N = True
USE_L10N = False

"""Timezone.
"""
TIME_ZONE = "Asia/Tokyo"
USE_TZ = True

"""Installed apps.
"""
INSTALLED_APPS = [
    "accounts.apps.Config",
    "corsheaders",
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]

"""Middlewares.
"""
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

"""Password validation rules.
"""
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

"""Templates.
"""
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

"""REST framework settings.
"""
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PAGINATION_CLASS": "accounts.pagination.Pagination",
    # "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    # "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "PAGE_SIZE": 25,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

"""CORS.
"""
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

"""Logging.
"""
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "normal": {
            "format": "{asctime} {levelname} {name}:{lineno} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "normal",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "django.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        # "django.db.backends": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
    },
}

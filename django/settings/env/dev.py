from ..common import *  # NOQA: F401,F403

"""CORE.
"""
DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": "5432",
    }
}

SECRET_KEY = "506445en4m34=iz$+hi#3v+h+a^z&t!v@#q)@2gum67!*9176v"

"""CORS.
"""
FRONTEND_HOST = "localhost:3000"
FRONTEND_ORIGIN = f"http://{FRONTEND_HOST}"

CORS_ORIGIN_WHITELIST = [FRONTEND_ORIGIN]
CSRF_TRUSTED_ORIGINS = [FRONTEND_HOST]

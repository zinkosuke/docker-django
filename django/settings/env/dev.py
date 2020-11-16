from ..common import *  # NOQA: F401,F403

"""Base.
"""
DEBUG = True
ALLOWED_HOSTS = ["*"]
FRONTEND_HOST = "localhost:3000"
FRONTEND_ORIGIN = f"http://{FRONTEND_HOST}"
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SECRET_KEY = "506445en4m34=iz$+hi#3v+h+a^z&t!v@#q)@2gum67!*9176v"
SECRET_TIMEOUT_SECONDS = 60 * 60 * 24

"""Email.
"""
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
FROM_EMAIL = None
ADMIN_EMAILS = ["admin@example.com"]

"""Database.
"""
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

"""CORS.
"""
CORS_ORIGIN_WHITELIST = [FRONTEND_ORIGIN]
CSRF_TRUSTED_ORIGINS = [FRONTEND_HOST]

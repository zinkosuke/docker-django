from django.urls import path
from rest_framework import routers

from . import views
from .apps import app_name  # NOQA: F401

router = routers.SimpleRouter()
router.register(r"users", views.UserReadOnlyViewSet)

# TODO
# User Register, EmailVerification
# User Edit, EmailChange
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password/change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password/reset_email/",
        views.PasswordResetEmailView.as_view(),
        name="password_reset_email",
    ),
    path(
        "password/reset/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
] + router.urls

from rest_framework import routers

from django.urls import path

from . import views
from .apps import app_name  # NOQA: F401

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet)

# TODO UserRegister, EmailChange, EmailVerification
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_forget/",
        views.PasswordForgetView.as_view(),
        name="password_forget",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
] + router.urls

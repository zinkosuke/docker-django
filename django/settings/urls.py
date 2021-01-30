from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny

from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("django_admin/", admin.site.urls),
    path(
        "docs/",
        get_schema_view(
            title="docker-django",
            description="API for all things …",
            version="0.1.0",
            permission_classes=[AllowAny],
        ),
        name="openapi-docs",
    ),
    path("v1/accounts/", include("accounts.urls", namespace="v1")),
]

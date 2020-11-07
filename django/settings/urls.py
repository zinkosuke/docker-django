from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("django_admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
]

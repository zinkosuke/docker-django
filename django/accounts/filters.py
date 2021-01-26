from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from . import models


class UserFilterSet(filters.FilterSet):
    username_like = filters.CharFilter(
        field_name="username", lookup_expr="contains"
    )
    none = filters.CharFilter(field_name="username", method="filter_none")

    class Meta:
        model = models.User
        fields = "__all__"

    def filter_none(self, queryset, name, value):
        return queryset.none()

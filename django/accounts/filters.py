from django_filters import rest_framework as filters

from . import models
from . import serializers


class UserFilterSet(filters.FilterSet):
    username_like = filters.CharFilter(
        field_name="username", lookup_expr="contains"
    )

    class Meta:
        model = models.User
        fields = serializers.UserReadOnlySerializer.Meta.fields

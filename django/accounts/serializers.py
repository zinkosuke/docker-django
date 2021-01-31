from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib import auth
from django.contrib.auth.forms import _unicode_ci_compare
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from . import email
from . import models


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "date_joined",
        )
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
        )

    def save(self):
        password = self.validated_data["password"]
        with transaction.atomic():
            instance = super().save()
            try:
                auth.password_validation.validate_password(password, instance)
            except DjangoValidationError as e:
                raise ValidationError({"password": e.messages})
            instance.set_password(password)
            instance.is_active = False
            instance.save()
            email.user_create(self.context["request"], instance)
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class BaseNewPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(
        max_length=128, required=True, write_only=True
    )
    new_password2 = serializers.CharField(
        max_length=128, required=True, write_only=True
    )

    def __init__(self, *args, **kwargs):
        self.user_cache = kwargs.pop("user", None)
        super().__init__(**kwargs)

    def validate(self, attrs):
        if self.user_cache is None:
            raise ValidationError(_("This account is inactive."))
        password1 = attrs.get("new_password1")
        password2 = attrs.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("The two password fields didn’t match."))
        auth.password_validation.validate_password(password2, self.user_cache)
        return attrs

    def save(self):
        self.user_cache.set_password(self.validated_data["new_password2"])
        self.user_cache.save()
        return self.user_cache


class ActivateSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        self.user_cache = models.User.url_decode(attrs.get("uid"))
        if self.user_cache is None:
            raise ValidationError(_("This account is inactive."))
        if not self.user_cache.compare_token(attrs.get("token")):
            raise ValidationError(_("This token is expired."))
        attrs = super().validate(attrs)
        return attrs

    def save(self):
        self.user_cache.is_active = True
        self.user_cache.save()
        return self.user_cache


class PasswordChangeSerializer(BaseNewPasswordSerializer):
    old_password = serializers.CharField(
        max_length=128, required=True, write_only=True
    )

    def validate_old_password(self, value):
        if not self.user_cache.check_password(value):
            raise ValidationError(
                _(
                    "Your old password was entered incorrectly. Please enter it again."
                )
            )
        return value


class PasswordForgetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(**kwargs)

    def save(self):
        email_value = self.validated_data["email"]
        for user in models.User.objects.filter(
            email__iexact=email_value, is_active=True
        ):
            if user.has_usable_password() and _unicode_ci_compare(
                email_value, user.email
            ):
                email.password_forget(self.request, user)


class PasswordResetSerializer(BaseNewPasswordSerializer):
    uid = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        self.user_cache = models.User.url_decode(attrs.get("uid"))
        if self.user_cache is None:
            raise ValidationError(_("This account is inactive."))
        if not self.user_cache.compare_token(attrs.get("token")):
            raise ValidationError(_("This token is expired."))
        attrs = super().validate(attrs)
        return attrs

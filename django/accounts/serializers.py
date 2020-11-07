from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import utils

User = auth.get_user_model()


class UserSerializer(serializers.ModelSerializer):
    method_field = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = [
            "password",
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_active",
            "last_login",
            "date_joined",
        ]

    def get_method_field(self, obj):
        return obj.pk


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username and password:
            self.user_cache = auth.authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                username_field = str(
                    User._meta.get_field(User.USERNAME_FIELD).verbose_name
                )
                raise ValidationError(
                    _(
                        "Please enter a correct %(username)s and password. Note that both "
                        "fields may be case-sensitive.",
                    ).replace("%(username)s", username_field),
                    code="invalid_login",
                )
            elif not self.user_cache.is_active:
                raise ValidationError(
                    _("This account is inactive."), code="inactive",
                )
        return attrs

    def save(self):
        auth.login(self.request, self.user_cache)
        return self.user_cache


class BaseNewPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128, required=True)
    new_password2 = serializers.CharField(max_length=128, required=True)

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


class PasswordChangeSerializer(BaseNewPasswordSerializer):
    old_password = serializers.CharField(max_length=128, required=True)

    def validate_old_password(self, value):
        if not self.user_cache.check_password(value):
            raise ValidationError(
                _(
                    "Your old password was entered incorrectly. Please enter it again."
                )
            )
        return value


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        return self.validated_data["email"]


class PasswordResetSerializer(BaseNewPasswordSerializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            uid = utils.urldecode_pk(attrs.get("uid"))
            self.user_cache = User._default_manager.get(pk=uid)
            if not utils.compare_user_token(
                self.user_cache, attrs.get("token")
            ):
                raise Exception()
        except Exception:
            raise ValidationError(_("This account is inactive."))
        attrs = super().validate(attrs)
        return attrs

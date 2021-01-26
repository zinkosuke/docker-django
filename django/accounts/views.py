from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import _unicode_ci_compare
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from . import email
from . import filters
from . import models
from . import permissions
from . import serializers


class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all().order_by("pk")
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilterSet


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAll]

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(request, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class LogoutView(views.APIView):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return Response({})


class PasswordChangeView(generics.GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class PasswordResetEmailView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetEmailSerializer
    permission_classes = [permissions.AllowAll]

    def get_users(self, email_value):
        email_field_name = models.User.get_email_field_name()
        active_users = models.User._default_manager.filter(
            **{"%s__iexact" % email_field_name: email_value, "is_active": True}
        )

        def __unicode_ci_compare(u):
            return _unicode_ci_compare(
                email_value, getattr(u, email_field_name)
            )

        return (
            u
            for u in active_users
            if u.has_usable_password() and __unicode_ci_compare(u)
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_value = serializer.save()
        for user in self.get_users(email_value):
            email.password_reset_email(request, user)
        return Response({})


class PasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [permissions.AllowAll]

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})

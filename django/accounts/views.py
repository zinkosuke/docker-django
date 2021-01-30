from rest_framework import generics
from rest_framework import views
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from django.contrib.auth.forms import _unicode_ci_compare

from . import email
from . import filters
from . import models
from . import permissions
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.User.objects.all().order_by("pk")
    filterset_class = filters.UserFilterSet

    def get_serializer_class(self):
        if self.action in {"update", "partial_update"}:
            return serializers.UserUpdateSerializer
        return serializers.UserReadOnlySerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return Response({}, status=204)


class PasswordChangeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=204)


class PasswordForgetView(generics.GenericAPIView):
    serializer_class = serializers.EmailSerializer

    def get_users(self, email_value):
        users = []
        for user in models.User.objects.filter(
            email__iexact=email_value, is_active=True
        ):
            if user.has_usable_password() and _unicode_ci_compare(
                email_value, user.email
            ):
                users.append(user)
        return users

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_value = serializer.save()
        for user in self.get_users(email_value):
            email.password_reset_email(request, user)
        return Response({}, status=204)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=204)

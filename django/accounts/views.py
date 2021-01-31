from rest_framework import views
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from . import filters
from . import models
from . import permissions
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by("pk")
    filterset_class = filters.UserFilterSet

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAll()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        if self.action in {"update", "partial_update"}:
            return serializers.UserUpdateSerializer
        return serializers.UserReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = serializers.UserReadSerializer(instance=instance)
        return Response(serializer.data, status=201)


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAll]

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
    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return Response({}, status=204)


class ActivateView(views.APIView):
    permission_classes = [permissions.AllowAll]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = serializers.UserReadSerializer(instance=instance)
        return Response(serializer.data, status=200)


class PasswordChangeView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordChangeSerializer(
            data=request.data, user=request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=204)


class PasswordForgetView(views.APIView):
    permission_classes = [permissions.AllowAll]

    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordForgetSerializer(
            request, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=204)


class PasswordResetView(views.APIView):
    permission_classes = [permissions.AllowAll]

    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=204)

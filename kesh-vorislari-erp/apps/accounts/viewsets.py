from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from apps.core.permissions import IsAdminRole

from .models import User
from .selectors import users_visible_to
from .serializers import RoleAwareTokenObtainPairSerializer, UserSerializer, UserWriteSerializer


class LoginView(TokenObtainPairView):
    serializer_class = RoleAwareTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    pass


class LogoutView(TokenBlacklistView):
    pass


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    search_fields = ("email", "first_name", "last_name")
    filterset_fields = ("role", "is_active")
    ordering_fields = ("last_name", "email", "date_joined")

    def get_queryset(self):
        return users_visible_to(self.request.user)

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            return UserWriteSerializer
        return UserSerializer

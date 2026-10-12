from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import LoginView, LogoutView, MeView, RefreshView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="api-users")

urlpatterns = [
    path("login/", LoginView.as_view(), name="api-login"),
    path("refresh/", RefreshView.as_view(), name="api-refresh"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
    path("me/", MeView.as_view(), name="api-me"),
    path("", include(router.urls)),
]

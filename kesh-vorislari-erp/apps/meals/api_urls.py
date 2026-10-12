from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import MealViewSet, MenuViewSet

router = DefaultRouter()
router.register("catalog", MealViewSet, basename="api-meals")
router.register("menus", MenuViewSet, basename="api-menus")

urlpatterns = [
    path("", include(router.urls)),
]

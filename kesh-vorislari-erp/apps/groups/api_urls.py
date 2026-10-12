from rest_framework.routers import DefaultRouter

from .viewsets import GroupViewSet

router = DefaultRouter()
router.register("", GroupViewSet, basename="api-groups")

urlpatterns = router.urls

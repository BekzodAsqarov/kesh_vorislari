from rest_framework.routers import DefaultRouter

from .viewsets import ChildViewSet

router = DefaultRouter()
router.register("", ChildViewSet, basename="api-children")

urlpatterns = router.urls

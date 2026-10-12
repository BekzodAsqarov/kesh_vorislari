from rest_framework.routers import DefaultRouter

from .viewsets import ActivityViewSet

router = DefaultRouter()
router.register("", ActivityViewSet, basename="api-activities")

urlpatterns = router.urls

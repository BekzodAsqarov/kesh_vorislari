from rest_framework.routers import DefaultRouter

from .viewsets import AttendanceViewSet

router = DefaultRouter()
router.register("", AttendanceViewSet, basename="api-attendance")

urlpatterns = router.urls

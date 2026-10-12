from rest_framework.routers import DefaultRouter

from .viewsets import DailyReportViewSet

router = DefaultRouter()
router.register("", DailyReportViewSet, basename="api-reports")

urlpatterns = router.urls

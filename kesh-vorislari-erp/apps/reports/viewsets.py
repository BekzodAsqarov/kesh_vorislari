from rest_framework import viewsets

from .permissions import DailyReportAccessPermission
from .selectors import reports_for_user
from .serializers import DailyReportSerializer


class DailyReportViewSet(viewsets.ModelViewSet):
    serializer_class = DailyReportSerializer
    permission_classes = [DailyReportAccessPermission]
    filterset_fields = ("date", "child", "mood")
    search_fields = ("child__first_name", "child__last_name", "note")
    ordering_fields = ("date", "mood")

    def get_queryset(self):
        return reports_for_user(self.request.user)

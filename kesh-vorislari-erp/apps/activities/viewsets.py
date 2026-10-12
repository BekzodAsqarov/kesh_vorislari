from rest_framework import viewsets

from .permissions import ActivityAccessPermission
from .selectors import activities_for_user
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [ActivityAccessPermission]
    filterset_fields = ("date", "group", "activity_type", "teacher")
    search_fields = ("title", "description", "location")
    ordering_fields = ("date", "start_time", "title")

    def get_queryset(self):
        return activities_for_user(self.request.user)

from rest_framework import viewsets

from .models import Group
from .permissions import GroupAccessPermission
from .selectors import groups_for_user
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [GroupAccessPermission]
    search_fields = ("name", "room", "description")
    filterset_fields = ("is_active", "teachers")
    ordering_fields = ("name", "age_min", "created_at")

    def get_queryset(self):
        return groups_for_user(self.request.user).prefetch_related("teachers", "children")

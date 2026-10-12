from rest_framework import viewsets

from .permissions import ChildAccessPermission
from .selectors import children_for_user
from .serializers import ChildSerializer


class ChildViewSet(viewsets.ModelViewSet):
    serializer_class = ChildSerializer
    permission_classes = [ChildAccessPermission]
    search_fields = ("first_name", "last_name", "allergies", "emergency_contact_name")
    filterset_fields = ("group", "gender", "is_active")
    ordering_fields = ("last_name", "first_name", "date_of_birth", "enrollment_date")

    def get_queryset(self):
        return children_for_user(self.request.user)

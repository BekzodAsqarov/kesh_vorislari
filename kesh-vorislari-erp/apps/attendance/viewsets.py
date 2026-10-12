from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import AttendanceAccessPermission
from .selectors import attendance_for_user
from .serializers import AttendanceSerializer, BulkAttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [AttendanceAccessPermission]
    filterset_fields = ("date", "status", "child", "child__group")
    search_fields = ("child__first_name", "child__last_name", "note")
    ordering_fields = ("date", "status", "child__last_name")

    def get_queryset(self):
        return attendance_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk(self, request):
        serializer = BulkAttendanceSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        items = serializer.save()
        return Response(AttendanceSerializer(items, many=True).data, status=status.HTTP_201_CREATED)

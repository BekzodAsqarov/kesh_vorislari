from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.permissions import IsAdminOrReadOnly

from .models import Meal, Menu
from .permissions import MenuAccessPermission
from .serializers import MealSerializer, MenuSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ("category", "is_active")
    search_fields = ("name", "ingredients", "allergens")
    ordering_fields = ("name", "category")


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.prefetch_related("items", "created_by").all()
    serializer_class = MenuSerializer
    permission_classes = [MenuAccessPermission]
    filterset_fields = ("date",)
    ordering_fields = ("date",)

    @action(detail=False, methods=["get"], url_path="weekly")
    def weekly(self, request):
        start = request.query_params.get("start")
        if start:
            from datetime import date as date_cls

            start_date = date_cls.fromisoformat(start)
        else:
            today = timezone.localdate()
            start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        menus = self.get_queryset().filter(date__range=(start_date, end_date)).order_by("date")
        return Response(
            {
                "start": start_date,
                "end": end_date,
                "results": MenuSerializer(menus, many=True).data,
            }
        )

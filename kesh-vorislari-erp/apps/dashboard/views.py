from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.activities.serializers import ActivitySerializer
from apps.meals.serializers import MenuSerializer

from .selectors import dashboard_payload


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = dashboard_payload(request.user)
        menu = data["menu"]
        return Response(
            {
                "today": data["today"],
                "children": data["children_count"],
                "groups": data["groups_count"],
                "teachers": data["teachers_count"],
                "attendance": data["attendance"],
                "activities": ActivitySerializer(data["activities"], many=True).data,
                "menu": MenuSerializer(menu).data if menu else None,
                "recent_reports": [
                    {
                        "id": report.id,
                        "child": report.child.full_name,
                        "date": report.date,
                        "mood": report.mood,
                    }
                    for report in data["recent_reports"]
                ],
            }
        )

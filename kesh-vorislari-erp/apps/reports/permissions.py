from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.children.selectors import user_can_access_child


class DailyReportAccessPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin or user.is_teacher

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user_can_access_child(user, obj.child):
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin or user.is_teacher

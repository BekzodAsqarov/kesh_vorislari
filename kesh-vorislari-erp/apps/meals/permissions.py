from rest_framework.permissions import SAFE_METHODS, BasePermission


class MenuAccessPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin

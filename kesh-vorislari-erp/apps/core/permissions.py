from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedAndActive(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and user.is_admin)


class IsTeacherRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and user.is_teacher)


class IsParentRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and user.is_parent)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin


class IsAdminOrTeacherWrite(BasePermission):
    """Admins have full access; teachers may write; parents are read-only."""

    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin or user.is_teacher

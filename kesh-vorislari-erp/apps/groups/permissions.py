from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.groups.selectors import groups_for_user


class GroupAccessPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_admin

    def has_object_permission(self, request, view, obj) -> bool:
        return groups_for_user(request.user).filter(pk=obj.pk).exists()

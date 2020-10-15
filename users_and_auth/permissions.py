from rest_framework.permissions import BasePermission, SAFE_METHODS


class Permission1(BasePermission):
    massage = "Нет прав на данное действие"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

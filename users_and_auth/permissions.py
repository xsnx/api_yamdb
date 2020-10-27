from rest_framework.permissions import BasePermission


class PermissionAdmin(BasePermission):
    massage = "Нет прав на данное действие"

    def has_permission(self, request, view):
        if (request.user.is_staff or
                request.user.is_superuser or
                request.user.is_admin):
            return True
        return False

from rest_framework.permissions import BasePermission, SAFE_METHODS


class Permission1(BasePermission):
    massage = "Нет прав на данное действие"

    def has_permission(self, request, view):
        if request.user.role == 'admin' or (
            request.user.is_staff or
            request.user.is_superuser):
            return True
        return False

    # def has_objects_permission(self, request, view, obj):
    #     if request.user.role == 'admin' or (
    #             request.user.is_staff or
    #             request.user.is_superuser or
    #             request.user == obj):
    #         return True
    #     return False


class Permission2(BasePermission):
    massage = "Нет прав на данное действие"

    def has_object_permission(self, request, view, obj):
        if request.user.role in ('admin',):
            return True
        return False

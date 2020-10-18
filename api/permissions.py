from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(
            (request.user.role == 'admin') or
            request.user.is_superuser
        )


class ReviewCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
                    request.user == obj.author or
                    request.user.role == 'admin' or
                    request.user.role == 'moderator' or
                    request.user.is_staff or request.user.is_superuser)

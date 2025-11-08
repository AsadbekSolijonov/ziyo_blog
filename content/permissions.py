from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    def has_permission(self, request, view):  # IsAuthenticated
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):  # IsOwnerOrSuperUser
        return bool(request.user == obj.user or request.user.is_superuser)

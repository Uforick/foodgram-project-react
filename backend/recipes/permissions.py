
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return all([
            request.user,
            request.user.is_authenticated,
            obj.author == request.user,
        ])

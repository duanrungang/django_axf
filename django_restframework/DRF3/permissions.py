from rest_framework.permissions import BasePermission

from DRF3.models import User


class UserLoginPermission(BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return isinstance(request.user, User)
        # return request.method in self.SAFE_METHODS or isinstance(request.user, User)

    def has_object_permission(self, request, view, obj):
        return obj.b_author.id == request.user.id


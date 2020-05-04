from rest_framework.permissions import BasePermission

from FruitGP2.models import FruitUser


class LoginPermission(BasePermission):
    def has_permission(self, request, view):
        # print(type(request.user))
        # print(FruitUser)
        return isinstance(request.user, FruitUser)

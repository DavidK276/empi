from http import HTTPMethod

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        return str(request.user.pk) == view.kwargs.get("pk", None)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CreateOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method == HTTPMethod.POST

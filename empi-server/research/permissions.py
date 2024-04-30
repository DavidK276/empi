from http import HTTPMethod

from rest_framework.permissions import BasePermission, SAFE_METHODS

from research.auth import ResearchAuthUser
from users.models import EmpiUser


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CreateOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method == HTTPMethod.POST


class AllowAllExceptList(BasePermission):

    def has_permission(self, request, view):
        return view.action != "list"


class ResearchPermission(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, EmpiUser) and request.user.is_staff:
            return True
        return view.action != "list" and isinstance(request.user, ResearchAuthUser)

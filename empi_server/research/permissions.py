from http import HTTPMethod

from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CreateOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method == HTTPMethod.POST


class AllowAllExceptList(BasePermission):

    def has_permission(self, request, view):
        return view.action != 'list'

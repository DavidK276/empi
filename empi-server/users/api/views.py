from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.response import Response

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.serializers import ValidationError


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            codes = e.get_codes()
            if "authorization" in codes.get("non_field_errors", []):
                status = 401
            else:
                status = 400
            return Response(serializer.errors, status=status)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format)

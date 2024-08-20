from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, inline_serializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnowLogoutView
from knox.views import LogoutAllView as KnowLogoutAllView
from rest_framework import permissions
from rest_framework.fields import DateTimeField, CharField
from rest_framework.response import Response

from .serializers import AuthTokenSerializer
from rest_framework.serializers import ValidationError

from ..serializers import UserSerializer


@extend_schema(
    request=inline_serializer(name="LoginRquestSerializer", fields={"email": CharField, "password": CharField}),
    responses=inline_serializer(
        name="LoginResponseSerializer", fields={"expiry": DateTimeField, "token": CharField, "user": UserSerializer}
    ),
)
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


@extend_schema(
    request=inline_serializer("LogoutRequestSerializer", fields={}),
    responses=inline_serializer(name="LogoutResponseSerializer", fields={}),
)
class LogoutView(KnowLogoutView):
    pass


@extend_schema(
    request=inline_serializer("LogoutAllRequestSerializer", fields={}),
    responses=inline_serializer(name="LogoutAllResponseSerializer", fields={}),
)
class LogoutAllView(KnowLogoutAllView):
    pass

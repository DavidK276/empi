from rest_framework import viewsets, permissions

from .models import EmpiUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.objects.get_queryset().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

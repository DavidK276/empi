from django.contrib.auth.models import Permission
from django.urls import include, path
from rest_framework import routers, viewsets, serializers
from users import views


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = []


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.get_queryset()
    serializer_class = PermissionSerializer


router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'lecturer', views.LecturerViewSet)
router.register(r'participant', views.ParticipantViewSet)
router.register(r'permission', PermissionViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls

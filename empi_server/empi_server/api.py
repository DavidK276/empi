from django.contrib.auth.models import Permission
from django.urls import include, path
from rest_framework import routers, viewsets, serializers
from users import views as users_views
from mailer import views as mailer_views


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = []


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.get_queryset()
    serializer_class = PermissionSerializer


router = routers.DefaultRouter()
router.register(r'permission', PermissionViewSet)

router.register(r'user', users_views.UserViewSet)
router.register(r'lecturer', users_views.LecturerViewSet)
router.register(r'participant', users_views.ParticipantViewSet)

router.register(r'email', mailer_views.EmailViewSet)
router.register(r'attachment', mailer_views.AttachmentViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls

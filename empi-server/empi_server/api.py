from django.contrib.auth.models import Permission
from django.urls import include, path
from rest_framework import routers, viewsets, serializers
from rest_framework.permissions import IsAdminUser

from emails import views as emails_views
from empi_settings import views as settings_views
from research import views as research_views
from users import views as users_views


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.get_queryset()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]


router = routers.DefaultRouter()
router.register(r"permission", PermissionViewSet)

router.register(r"user", users_views.UserViewSet)
router.register(r"participant", users_views.ParticipantViewSet)
router.register(r"attr", users_views.AttributeViewSet)

router.register(r"email", emails_views.EmailViewSet)
router.register(r"attachment", emails_views.AttachmentViewSet)

router.register(r"research-user", research_views.ResearchUserViewSet, basename="research-user")
router.register(r"research-admin", research_views.ResearchAdminViewSet, basename="research-admin")

router.register(r"participation", research_views.ParticipationViewSet, basename="participation")
router.register(r"anon-participation", research_views.AnonymousParticipationViewSet, basename="anon-participation")

router.register(r"settings", settings_views.SettingsViewSet)

urlpatterns = [
    path("rf-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("auth/", include("users.urls")),
]

urlpatterns += router.urls

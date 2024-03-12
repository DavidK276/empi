from django.contrib.auth.models import Permission
from django.urls import include, path
from rest_framework import routers, viewsets, serializers
from rest_framework.permissions import IsAdminUser
from users import views as users_views
from emails import views as emails_views
from research import views as research_views


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
# router.register(r'attr-value', users_views.AttributeValueViewSet)

router.register(r"email", emails_views.EmailViewSet)
router.register(r"attachment", emails_views.AttachmentViewSet)

router.register(r"research", research_views.ResearchViewSet)
router.register(r"appointment", research_views.AppointmentViewSet)
router.register(r"participation", research_views.ParticipationViewSet)

urlpatterns = [
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("rest-auth/", include("dj_rest_auth.urls")),
]

urlpatterns += router.urls

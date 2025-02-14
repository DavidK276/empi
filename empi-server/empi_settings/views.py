from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser

from empi_settings.models import Settings
from empi_settings.serializers import SettingsSerializer
from research.permissions import ReadOnly


class SettingsViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Settings.objects.get_queryset()
    serializer_class = SettingsSerializer
    permission_classes = [ReadOnly | IsAdminUser]
    lookup_field = "name"
    pagination_class = None

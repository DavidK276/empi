from rest_framework import serializers

from empi_settings.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ["name", "value", "type"]
        extra_kwargs = {"name": {"read_only": True}, "type": {"read_only": True}}

from rest_framework import serializers

from . import models


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = "__all__"


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Attachment
        fields = "__all__"

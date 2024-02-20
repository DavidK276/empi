from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models as user_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_models.EmpiUser
        exclude = ['password']

from rest_framework import serializers
from .models import *

class TeamsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Teams
        fields = ("__all__")
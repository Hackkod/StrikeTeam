from rest_framework import serializers
from .models import *


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'


class TeammatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teammates
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        extra_kwargs = {'teammate_name': {'read_only': True}}
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']    


from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from users.serializer import *

class service_provider_serializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    user = user_serializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = service_provider
        fields = '__all__'
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user = instance.user
        user.email = validated_data.pop('email', user.email)
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.save()

        return super().update(instance, validated_data)

    def create(self, validated_data):
        user = self.context['request'].user
        user.email = validated_data.pop('email', user.email)
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.save()

        return service_provider.objects.create(**validated_data)
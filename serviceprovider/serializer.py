
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class service_provider_serializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = service_provider
        fields = ['id', 'full_name', 'service_center_name', 'address', 'email', 'password']

    def create(self, validated_data):
        email = validated_data.pop('email')
        print(email)
        password = validated_data.pop('password')
       
        user = User.objects.create(
            email=email,
            is_service_provider=True,
            password=make_password(password)  # Encrypt password
        )

        service_provider_instance = service_provider.objects.create(user=user, **validated_data)
        return service_provider_instance

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        if email:
            instance.user.email = email
        if password:
            instance.user.password = make_password(password)  # Encrypt new password

        instance.user.save()
        return super().update(instance, validated_data)

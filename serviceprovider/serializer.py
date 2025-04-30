
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class service_provider_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = service_provider
        fields = '__all__'
        read_only_fields = ['user']

    image = serializers.ImageField(required=False, allow_null=True)
    
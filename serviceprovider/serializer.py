
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class service_provider_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = service_provider
        fields = ['full_name', 'service_center_name', 'address']

    
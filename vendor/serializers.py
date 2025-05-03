# serializers.py

from rest_framework import serializers
from .models import vendor_kyc

class VendorKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendor_kyc
        fields = ['id', 'user', 'image', 'document_type', 'document_image', 'approved']
        read_only_fields = ['user', 'approved']

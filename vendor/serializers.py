# serializers.py

from rest_framework import serializers
from .models import *

class VendorKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendor_kyc
        fields = ['id', 'user', 'image', 'document_type', 'document_image', 'approved']
        read_only_fields = ['user', 'approved']



class VendorWalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendor_wallet_transaction
        fields = '__all__'
        read_only_fields = ['wallet', 'created_at']

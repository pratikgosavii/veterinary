from rest_framework import serializers
from .models import *



from rest_framework import serializers
from .models import *


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = pet
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['owner'] = request.user
        return super().create(validated_data)
    
    
class consultation_appointment_Serializer(serializers.ModelSerializer):
    
    pet = serializers.PrimaryKeyRelatedField(
        many=True, queryset=consultation_appointment._meta.get_field('pet').remote_field.model.objects.all()
    )

    symptom = serializers.PrimaryKeyRelatedField(
        many=True, queryset=consultation_appointment._meta.get_field('symptom').remote_field.model.objects.all()
    )

    class Meta:
        model = consultation_appointment
        fields = ['id', 'pet', 'symptom', 'doctor', 'date', 'payment_status']
        read_only_fields = ['user']

        def create(self, validated_data):
            request = self.context['request']
            validated_data['user'] = request.user
            return super().create(validated_data)

class vaccination_appointment_Serializer(serializers.ModelSerializer):
    
    pet = serializers.PrimaryKeyRelatedField(
        many=True, queryset=vaccination_appointment._meta.get_field('pet').remote_field.model.objects.all()
    )

    vaccination = serializers.PrimaryKeyRelatedField(
        many=True, queryset=vaccination_appointment._meta.get_field('vaccination').remote_field.model.objects.all()
    )

    class Meta:
        model = vaccination_appointment
        fields = ['id', 'pet', 'vaccination', 'doctor', 'date', 'payment_status']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)

class test_booking_Serializer(serializers.ModelSerializer):
    
    pet = serializers.PrimaryKeyRelatedField(
        many=True, queryset=test_booking._meta.get_field('pet').remote_field.model.objects.all()
    )

    test = serializers.PrimaryKeyRelatedField(
        many=True, queryset=test_booking._meta.get_field('test').remote_field.model.objects.all()
    )

    class Meta:
        model = test_booking
        fields = ['id', 'pet', 'test', 'doctor', 'date', 'payment_status']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    

from masters.serializers import *

class CartSerializer(serializers.ModelSerializer):
    product = product_serializer(read_only=True)

    class Meta:
        model = cart
        fields = ['id', 'product', 'quantity', 'added_at']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
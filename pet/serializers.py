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
        fields = ['id', 'pet', 'test', 'doctor', 'date', 'payment_status', 'report']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    

from masters.serializers import *

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType



class CartSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(write_only=True)  # e.g., "product", "vaccination"
    object_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = cart
        fields = ['item_type', 'object_id', 'quantity']

    def validate(self, data):
        model = data['item_type'].lower()
        try:
            content_type = ContentType.objects.get(model=model)
            model_class = content_type.model_class()
            model_class.objects.get(id=data['object_id'])  # Ensure object exists
            data['content_type'] = content_type
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(f"No model named '{model}' exists.")
        except model_class.DoesNotExist:
            raise serializers.ValidationError(f"{model.title()} with ID {data['object_id']} not found.")
        return data

    def create(self, validated_data):
        return cart.objects.create(
            user=self.context['request'].user,
            content_type=validated_data['content_type'],
            object_id=validated_data['object_id'],
            quantity=validated_data['quantity']
        )

class AddToCartSerializer(serializers.Serializer):
    item_type = serializers.ChoiceField(choices=['product', 'service', 'vaccination', 'test'])
    object_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = ['id', 'products', 'total', 'created_at']

        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
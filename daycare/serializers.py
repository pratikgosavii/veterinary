from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from masters.serializers import *

from users.serializer import *

class day_care_serializer(serializers.ModelSerializer):
    # For POST

    amenities = serializers.StringRelatedField(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=amenity.objects.all(), write_only=True, required=False
    )

    email = serializers.CharField(source="user.email", read_only=True)
    mobile = serializers.CharField(source="user.mobile", required=False)

    class Meta:
        model = day_care
        fields = [
            'id', 'user', 'name', 'images', 'location', 'description',
            'price_full_day', 'price_half_day',
            'amenities', 'amenity_ids',
            'rating', 'email', 'mobile'
        ]
        extra_kwargs = {'user': {'read_only': True}}


    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if day_care.objects.filter(user=user).exists():
            raise serializers.ValidationError("You have already registered a daycare.")

        amenities = validated_data.pop('amenity_ids', [])

        # 🛠 Fix: Manually rebuild food_menus from request.POST (because of form-data)
      
        instance = day_care.objects.create(**validated_data)

        if amenities:
            instance.amenities.set(amenities)

       
        return instance


class DayCareFoodMenuSerializer(serializers.ModelSerializer):
    
    amenities = serializers.StringRelatedField(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=amenity.objects.all(), write_only=True, required=False
    )

    email = serializers.CharField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", write_only=True, required=False)
    last_name = serializers.CharField(source="user.last_name", write_only=True, required=False)
    mobile = serializers.CharField(source="user.mobile", required=False)

    class Meta:
        model = day_care
        fields = [
            'id', 'user', 'name', 'images', 'location', 'description',
            'price_full_day', 'price_half_day',
            'amenities', 'amenity_ids',
            'rating', 'email', 'first_name', 'last_name', 'mobile'
        ]
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if day_care.objects.filter(user=user).exists():
            raise serializers.ValidationError("You have already registered a daycare.")

        amenities = validated_data.pop('amenity_ids', [])

        # Manually update user fields if provided in the request
        user.email = validated_data.pop('user', {}).get('email', user.email)
        user.first_name = validated_data.pop('user', {}).get('first_name', user.first_name)
        user.last_name = validated_data.pop('user', {}).get('last_name', user.last_name)
        user.save()

        instance = day_care.objects.create(**validated_data)

        if amenities:
            instance.amenities.set(amenities)

        return instance

    def update(self, instance, validated_data):
        user = instance.user

        # Update user fields if provided
        user.email = validated_data.pop('user', {}).get('email', user.email)
        user.first_name = validated_data.pop('user', {}).get('first_name', user.first_name)
        user.last_name = validated_data.pop('user', {}).get('last_name', user.last_name)
        user.save()

        return super().update(instance, validated_data)
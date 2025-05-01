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
  
    class Meta:
        model = DayCareFoodMenu
        fields = '__all__'
        extra_kwargs = {'daycare': {'read_only': True}}

    def create(self, validated_data):
        request = self.context['request']
        
        try:
            daycare = day_care.objects.get(user=request.user)
        except day_care.DoesNotExist:
            raise serializers.ValidationError("You are not registered with any daycare.")
        
        validated_data['daycare'] = daycare
        instance = DayCareFoodMenu.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        # standard single update
        return super().update(instance, validated_data)

    def bulk_update(self, data_list):
        """
        Custom method to handle bulk updates.
        """
        updated_instances = []

        for item in data_list:
            try:
                instance = DayCareFoodMenu.objects.get(id=item['id'])

                # Remove 'id' from data before passing to serializer
                item_data = item.copy()
                item_data.pop('id', None)

                serializer = DayCareFoodMenuSerializer(
                    instance, data=item_data, partial=True, context=self.context
                )

                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_instances.append(serializer.instance)
            except DayCareFoodMenu.DoesNotExist:
                continue

        return updated_instances
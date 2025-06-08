from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from masters.serializers import *

from users.serializer import *

class day_care_serializer(serializers.ModelSerializer):
    # For POST

    amenities = serializers.StringRelatedField(many=True, read_only=True)
    user_details = user_serializer(source='user', read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=amenity.objects.all(), write_only=True, required=False
    )

    email = serializers.CharField(source="user.email", read_only=True)
    mobile = serializers.CharField(source="user.mobile", required=False)

    class Meta:
        model = day_care
        fields = [
            'id', 'user', 'user_details', 'name', 'images', 'location', 'description',
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
            daycare = day_care.objects.get(user=request.user, is_active=True)
        except day_care.DoesNotExist:
            raise serializers.ValidationError("You are not registered with any active daycare.")
        
        validated_data['daycare'] = daycare
        return DayCareFoodMenu.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Standard update logic
        return super().update(instance, validated_data)

    def bulk_update(self, data_list):
        """
        Custom method to handle bulk updates via POST or PUT.
        Expects list of dicts with 'id' and the fields to update.
        """
        updated_instances = []
        user = self.context['request'].user

        for item in data_list:
            try:
                # Only update items belonging to the user's daycare
                instance = DayCareFoodMenu.objects.get(id=item['id'], daycare__user=user)

                item_data = item.copy()
                item_data.pop('id', None)  # remove id before passing to serializer

                serializer = DayCareFoodMenuSerializer(
                    instance, data=item_data, partial=True, context=self.context
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_instances.append(serializer.instance)

            except DayCareFoodMenu.DoesNotExist:
                # Skip items not found or not belonging to user
                continue
            except Exception as e:
                # Optional: log or handle unexpected errors
                continue

        return updated_instances
from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from masters.serializers import *

from users.serializer import *

class day_care_serializer(serializers.ModelSerializer):
    # For POST
    email = serializers.EmailField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    user = user_serializer(read_only=True)
    amenities = amenity_serializer(many=True, read_only=True)

    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=amenity.objects.all(), write_only=True, required=False
    )

    email_display = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = day_care
        fields = '__all__'
        read_only_fields = ['user', 'is_active']

    def update(self, instance, validated_data):
        user = instance.user
        user.email = validated_data.pop('email', user.email)
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.save()

        amenities = validated_data.pop('amenity_ids', None)
        instance = super().update(instance, validated_data)
        if amenities is not None:
            instance.amenities.set(amenities)

        return instance

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if day_care.objects.filter(user=user).exists():
            raise serializers.ValidationError("You have already registered a daycare.")

        # update user details
        user.email = validated_data.pop('email', user.email)
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.save()

        amenities = validated_data.pop('amenity_ids', [])

        # ✅ Call super().create so image + other fields are handled correctly
        instance = super().create({**validated_data, "user": user})

        if amenities:
            instance.amenities.set(amenities)

        return instance
    

class DayCareFoodMenuSerializer(serializers.ModelSerializer):

    food_menu_details = food_menu_serializer(source='food_menu', read_only=True)  # for GET
    food_menu_id = serializers.PrimaryKeyRelatedField(
        queryset=food_menu.objects.all(), write_only=True, source='food_menu'  # use model here
    )

    class Meta:
        model = DayCareFoodMenu
        fields = ['id', 'daycare', 'food_menu_details', 'food_menu_id', 'custom_price']
        extra_kwargs = {'daycare': {'read_only': True}}

    def create(self, validated_data):
        request = self.context['request']
        try:
            daycare = day_care.objects.get(user=request.user, is_active=True)
        except day_care.DoesNotExist:
            raise serializers.ValidationError("You are not registered with any active daycare.")
        
        food_menu = validated_data.get('food_menu')
        
        # Check if this food_menu already exists for this daycare
        if DayCareFoodMenu.objects.filter(daycare=daycare, food_menu=food_menu).exists():
            raise serializers.ValidationError("This food menu is already added to your daycare.")
        
        validated_data['daycare'] = daycare
        return DayCareFoodMenu.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Get user daycare
        request = self.context['request']
        try:
            daycare = day_care.objects.get(user=request.user, is_active=True)
        except day_care.DoesNotExist:
            raise serializers.ValidationError("You are not registered with any active daycare.")
        
        food_menu = validated_data.get('food_menu')
        if food_menu and food_menu != instance.food_menu:
            # Check if new food_menu already exists for daycare
            if DayCareFoodMenu.objects.filter(daycare=daycare, food_menu=food_menu).exclude(id=instance.id).exists():
                raise serializers.ValidationError("This food menu is already added to your daycare.")
        
        return super().update(instance, validated_data)
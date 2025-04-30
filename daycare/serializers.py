from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from masters.serializers import *



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
    
    food_menu_id = serializers.PrimaryKeyRelatedField(
        queryset=food_menu.objects.all(), source='food_menu', write_only=True
    )
    food_menu = food_menu_serializer(read_only=True)
    daycare = day_care_serializer(read_only=True)


    class Meta:
        model = DayCareFoodMenu
        fields = ['food_menu', 'food_menu_id', 'custom_price', 'daycare']


    def create(self, validated_data):
        
        print(validated_data)
        validated_data.pop('daycare', None)
        print(validated_data)
        
        # Get day_care from request context (set in the view)
        request = self.context.get('request')
        user = request.user
        try:
            daycare = day_care.objects.get(user=user, is_active=True)
        except day_care.DoesNotExist:
            raise serializers.ValidationError("No active daycare found for this user.")
        
        return DayCareFoodMenu.objects.create(daycare=daycare, **validated_data)


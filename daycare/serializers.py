from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from masters.serializers import *


class DayCareFoodMenuSerializer(serializers.ModelSerializer):
    food_menu_id = serializers.PrimaryKeyRelatedField(
        queryset=food_menu.objects.all(), source='food_menu', write_only=True
    )
    food_menu = food_menu_serializer(read_only=True)

    class Meta:
        model = DayCareFoodMenu
        fields = ['food_menu', 'food_menu_id', 'custom_price']


class day_care_serializer(serializers.ModelSerializer):
    # For POST
    food_menus = DayCareFoodMenuSerializer(many=True, write_only=True)

    # For GET
    food_menus_data = DayCareFoodMenuSerializer(
        source='daycarefoodmenu_set', many=True, read_only=True
    )

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
            'food_menus', 'food_menus_data',
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
        food_menus_data = []
        i = 0
        while True:
            food_menu_id = request.POST.get(f'food_menus[{i}][food_menu]')
            custom_price = request.POST.get(f'food_menus[{i}][custom_price]')
            if food_menu_id is None:
                break
            food_menus_data.append({
                'food_menu': food_menu_id,
                'custom_price': custom_price,
            })
            i += 1

        instance = day_care.objects.create(**validated_data)

        if amenities:
            instance.amenities.set(amenities)

        for item in food_menus_data:
            DayCareFoodMenu.objects.create(
                daycare=instance,
                food_menu_id=item['food_menu'],  # notice: using _id
                custom_price=item['custom_price']
            )

        return instance



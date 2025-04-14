from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from masters.serializers import *



class day_care_serializer(serializers.ModelSerializer):
    
    
    amenities = amenity_serializer(many=True, read_only=True)  # for GET
    amenity_ids = serializers.PrimaryKeyRelatedField(  # for POST/PUT
        many=True, queryset=amenity.objects.all(), write_only=True, required=False
    )
    email = serializers.CharField(source="user.email", read_only=True)
    mobile = serializers.CharField(source="user.mobile", required=False)

    class Meta:
        model = day_care
        fields = [
            'id', 'user', 'name', 'images', 'location', 
            'description', 'price_per_hour', 'price_per_day', 
            'amenities', 'amenity_ids', 'rating', 'email', 'mobile'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if day_care.objects.filter(user=user).exists():
            raise serializers.ValidationError("You have already registered a daycare.")

        amenities = validated_data.pop('amenity_ids', [])
        mobile = validated_data.pop('user', {}).get('mobile', None)
        if mobile:
            user.mobile = mobile
            user.save()

        instance = day_care.objects.create(user=user, **validated_data)
        if amenities:
            instance.amenities.set(amenities)
        return instance

    def update(self, instance, validated_data):
        amenities = validated_data.pop('amenity_ids', None)
        mobile = validated_data.pop('user', {}).get('mobile', None)
        if mobile:
            instance.user.mobile = mobile
            instance.user.save()
        if amenities is not None:
            instance.amenities.set(amenities)
        return super().update(instance, validated_data)


class DayCareBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = day_care_booking
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)



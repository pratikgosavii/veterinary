from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import day_care

class day_care_serializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = day_care
        fields = [
            'id', 'user', 'name', 'images', 'location', 
            'description', 'price_per_hour', 'price_per_day', 
            'amenities', 'rating', 'email', 'password'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'amenities': {'required': False},  # Optional field
        }

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password', None)
        
        # Check if user exists (optional, adjust logic as needed)
      
        # Create day_care instance linked to the user
        user = User.objects.create(
            email=email,
            is_day_care=True,
            password=make_password(password)  # Encrypt password
        )

        day_care_instance = day_care.objects.create(user=user, **validated_data)
        return day_care_instance

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        # Update user email/password if provided
        if email:
            instance.user.email = email
        if password:
            instance.user.password = make_password(password)
        
        instance.user.save()
        return super().update(instance, validated_data)
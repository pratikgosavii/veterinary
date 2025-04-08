from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from .models import day_care

class day_care_serializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")
    mobile = serializers.CharField(source="user.mobile")
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = day_care
        fields = [
            'id', 'user', 'name', 'images', 'location', 
            'description', 'price_per_hour', 'price_per_day', 
            'amenities', 'rating', 'email', 'mobile', 'password'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'amenities': {'required': False},  # Optional field
        }

    def create(self, validated_data):
        
        print(validated_data)

        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        mobile = user_data.get('mobile')
        password = validated_data.pop('password', None)
        
        # Check if user exists (optional, adjust logic as needed)
      
        # Create day_care instance linked to the user
        user = User.objects.create(
            mobile=mobile,
            email=email,
            is_daycare=True,
            password=make_password(password)  # Encrypt password
        )

        day_care_instance = day_care.objects.create(user=user, **validated_data)
        return day_care_instance

    def update(self, instance, validated_data):
        mobile = validated_data.pop('mobile', None)
        password = validated_data.pop('password', None)

        # Update user mobile/password if provided
        if mobile:
            instance.user.mobile = mobile
        if password:
            instance.user.password = make_password(password)
        
        instance.user.save()
        return super().update(instance, validated_data)
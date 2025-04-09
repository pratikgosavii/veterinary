
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class doctor_serializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(write_only=True, required=False)
    available_from = serializers.TimeField(format="%I:%M %p")  # e.g., 06:00 AM
    available_to = serializers.TimeField(format="%I:%M %p") 
    class Meta:
        model = doctor
        fields = ['id', 'name', 'experience', 'title', 'degree', 'mobile_no', 'available_from', 'available_to', 'address', 'email', 'password']

    def create(self, validated_data):
        email = validated_data.pop('email')
        print(email)
        password = validated_data.pop('password')
       
        user = User.objects.create(
            email=email,
            is_doctor=True,
            password=make_password(password)  # Encrypt password
        )

        doctor_instance = doctor.objects.create(user=user, **validated_data)
        return doctor_instance

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        if email:
            instance.user.email = email
        if password:
            instance.user.password = make_password(password)  # Encrypt new password

        instance.user.save()
        return super().update(instance, validated_data)

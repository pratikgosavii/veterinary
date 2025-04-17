
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
        fields = ['id', 'name', 'image', 'experience', 'title', 'degree', 'mobile_no', 'available_from', 'available_to', 'address', 'email', 'password']

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

from rest_framework import serializers
from .models import ConsultationAppointmentReport, OnlineConsultationAppointmentReport, TestBookingReport
from doctor.models import consultation_appointment, online_consultation_appointment
from pet.models import test_booking

class ConsultationAppointmentReportSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(
        queryset=consultation_appointment.objects.all(),
        write_only=True
    )
    appointment_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConsultationAppointmentReport
        fields = ['id', 'appointment', 'appointment_details', 'file', 'uploaded_at']

    def get_appointment_details(self, obj):
        from pet.serializers import consultation_appointment_Serializer
        return consultation_appointment_Serializer(obj.appointment).data


class OnlineConsultationAppointmentReportSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(
        queryset=online_consultation_appointment.objects.all(),
        write_only=True
    )
    appointment_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OnlineConsultationAppointmentReport
        fields = ['id', 'appointment', 'appointment_details', 'file', 'uploaded_at']

    def get_appointment_details(self, obj):
        from pet.serializers import online_consultation_appointment_Serializer
        return online_consultation_appointment_Serializer(obj.appointment).data


class TestBookingReportSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(
        queryset=test_booking.objects.all(),
        write_only=True
    )
    booking_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TestBookingReport
        fields = ['id', 'report', 'booking', 'booking_details', 'uploaded_at']

    def get_booking_details(self, obj):
        from pet.serializers import test_booking_Serializer
        return test_booking_Serializer(obj.booking).data


from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import *

class doctor_serializer(serializers.ModelSerializer):

    class Meta:
        model = doctor
        fields = '__all__'
        read_only_fields = ['user']

    image = serializers.ImageField(required=False, allow_null=True)
    

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

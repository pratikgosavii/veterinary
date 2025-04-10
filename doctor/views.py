from django.shortcuts import render

# Create your views here.




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from doctor.filters import *

class doctor_login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if user exists and is a customer
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        print()

        if not user.is_pharmassist:  # Check if `is_customer` is True
            return Response({"error": "Access denied. Not a pharmassist."}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"id": user.id, "email": user.email}
        }, status=status.HTTP_200_OK)


from .serializer import *
from rest_framework import generics, permissions

class doctor_signup(generics.CreateAPIView):
    
    queryset = doctor.objects.all()
    serializer_class = doctor_serializer



from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

class get_doctor(ListAPIView):
    queryset = doctor.objects.all()
    serializer_class = doctor_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorFilter   # enables filtering on all fields


from pet.models import *
from pet.serializers import *
from users.permissions import *






class list_consultation_appointment(ListAPIView):
    serializer_class = consultation_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']  # add more as needed

    def get_queryset(self):
        doctor_instance = self.request.user.doctor
        return consultation_appointment.objects.filter(doctor=doctor_instance).distinct()



class list_vaccination_appointment(ListAPIView):
    serializer_class = vaccination_appointment_Serializer
    permission_classes = [IsDoctor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']  # add more as needed

    def get_queryset(self):
        # Get doctor instance linked to the logged-in user
        doctor_instance = self.request.user.doctor
        return vaccination_appointment.objects.filter(doctor=doctor_instance).distinct()
    


class list_test_booking(ListAPIView):
    serializer_class = test_booking_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']  # add more as needed

    def get_queryset(self):
        doctor_instance = self.request.user.doctor
        return test_booking.objects.filter(doctor=doctor_instance).distinct()

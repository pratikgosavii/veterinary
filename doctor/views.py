from django.shortcuts import render

# Create your views here.




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.generics import CreateAPIView, ListAPIView
from .models import day_care_booking


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated

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
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser


class DoctorViewSet(viewsets.ModelViewSet):

    queryset = doctor.objects.all()
    serializer_class = doctor_serializer
    parser_classes = [MultiPartParser, JSONParser]  # ✅ Allow both JSON and form-data

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        doctor_obj = self.get_object()
        doctor_obj.is_active = False
        doctor_obj.save()
        return Response({"message": "Doctor deactivated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        doc = self.get_object()
        doc.is_active = True
        doc.save()
        return Response({"message": "Doctor reactivated"}, status=status.HTTP_200_OK)



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





class ConsultationReportView(APIView):

    permission_classes = [IsDoctor]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        reports = ConsultationAppointmentReport.objects.all()
        serializer = ConsultationAppointmentReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsultationAppointmentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        report_id = request.data.get('report_id')
        if not report_id:
            return Response({'error': 'report_id required'}, status=400)

        try:
            report = ConsultationAppointmentReport.objects.get(id=report_id)
            report.delete()
            return Response({'status': 'deleted'})
        except ConsultationAppointmentReport.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)


class OnlineConsultationReportView(APIView):

    permission_classes = [IsDoctor]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        reports = OnlineConsultationAppointmentReport.objects.all()
        serializer = OnlineConsultationAppointmentReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OnlineConsultationAppointmentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        report_id = request.data.get('report_id')
        if not report_id:
            return Response({'error': 'report_id required'}, status=400)

        try:
            report = OnlineConsultationAppointmentReport.objects.get(id=report_id)
            report.delete()
            return Response({'status': 'deleted'})
        except OnlineConsultationAppointmentReport.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)


class TestReportView(APIView):

    permission_classes = [IsDoctor]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        reports = TestBookingReport.objects.all()
        serializer = TestBookingReportSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = TestBookingReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        report_id = request.data.get('report_id')
        if not report_id:
            return Response({'error': 'report_id required'}, status=400)

        try:
            report = TestBookingReport.objects.get(id=report_id)
            report.delete()
            return Response({'status': 'deleted'})
        except TestBookingReport.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.db.models import Count
# from petprofile.models import *




from rest_framework.response import Response
from rest_framework import viewsets
from itertools import chain
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware, is_naive
from rest_framework.generics import CreateAPIView, ListAPIView
from pet.serializers import *
from doctor.serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from itertools import chain
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware, is_naive


class all_open_bookings(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        appointments = []

        def serialize(qs, appt_type):
            return [
                {
                    "id": obj.id,
                    "type": appt_type,
                    "status": obj.status,
                    "date": str(getattr(obj, "date", None)),  # Adjust as needed
                    "amount": obj.amount,  # Adjust as needed
                    "name": obj.user.first_name + obj.user.last_name,  # Adjust as needed
                }
                for obj in qs
            ]

        if hasattr(user, 'is_doctor'):
            online_consultations = online_consultation_appointment.objects.filter(status="open")
            vaccinations = vaccination_appointment.objects.filter(status="open")
            tests = test_booking.objects.filter(status="open")

            appointments = (
                serialize(online_consultations, "online_consultation") +
                serialize(vaccinations, "vaccination") +
                serialize(tests, "test")
            )

        elif hasattr(user, 'is_daycare'):
            daycares = day_care_booking.objects.filter(status="open")
            appointments = serialize(daycares, "daycare")

        elif hasattr(user, 'is_service_provider'):
            services = service_booking.objects.filter(status="open")
            appointments = serialize(services, "service")

        else:
            return Response({"detail": "Invalid user type"}, status=400)

        return Response({"appointments": appointments})
    

from datetime import date, datetime

class all_vendor_bookings(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        today = date.today()

        upcoming_appointments = []
        past_appointments = []

        def serialize(qs, appt_type):
            return [
                {
                    "id": obj.id,
                    "type": appt_type,
                    "status": obj.status,
                    "date": obj.date,
                    "amount": getattr(obj, 'amount', None),
                    "name": f"{obj.user.first_name} {obj.user.last_name}",
                }
                for obj in qs
            ]

        all_appointments = []

        if hasattr(user, 'is_doctor'):
            print('----------------1-----------------')
            doctor_instance = doctor.objects.get(user=user)
            all_appointments += (
                serialize(online_consultation_appointment.objects.filter(doctor=doctor_instance), "online_consultation") +
                serialize(consultation_appointment.objects.filter(doctor=doctor_instance), "consultation") +
                serialize(vaccination_appointment.objects.filter(doctor=doctor_instance), "vaccination") +
                serialize(test_booking.objects.filter(doctor=doctor_instance), "test")
            )


        elif hasattr(user, 'is_daycare'):
            print('----------------2-----------------')

            daycare_instance = day_care.objects.get(user=user)
            all_appointments += serialize(day_care_booking.objects.filter(daycare=daycare_instance), "daycare")

        elif hasattr(user, 'is_service_provider'):
            print('----------------3-----------------')

            service_provider_instance = service_provider.objects.get(user=user)
            all_appointments += serialize(service_booking.objects.filter(service_provider=service_provider_instance), "service")

        else:
            return Response({"detail": "Invalid user type"}, status=400)

        for appt in all_appointments:
            appt_date = appt["date"]
           
            if appt_date and appt_date.date() >= today:
                print('------------------------')
                upcoming_appointments.append(appt)
            else:
                past_appointments.append(appt)

        return Response({
            "upcoming": upcoming_appointments,
            "past": past_appointments
        })
    




class all_bookings_count(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        

        user = request.user
        

        if hasattr(user, 'is_doctor'):

        
            doctor_instance = doctor.objects.get(user = request.user)  # Assuming doctor is related to User

            # Consultation Appointment Report
            consultation_counts = consultation_appointment.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))

            # Online Consultation Appointment Report
            online_counts = online_consultation_appointment.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))

            # Test Booking Report
            vaccination_counts = vaccination_appointment.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))


            # Test Booking Report
            test_counts = test_booking.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))

            def to_status_dict(queryset):
                data = {'accepted': 0, 'completed': 0, 'cancelled': 0}
                for entry in queryset:
                    status = entry['status'].lower()
                    if status in data:
                        data[status] += entry['total']
                return data

            # Individual breakdown
            consultation = to_status_dict(consultation_counts)
            online = to_status_dict(online_counts)
            test = to_status_dict(test_counts)
            vaccination = to_status_dict(vaccination_counts)

            # Total combined
            combined = {
                "accepted": consultation['accepted'] + online['accepted'] + test['accepted'] + vaccination['accepted'],
                "completed": consultation['completed'] + online['completed'] + test['completed'] + vaccination['completed'],
                "cancelled": consultation['cancelled'] + online['cancelled'] + test['cancelled'] + vaccination['cancelled'] ,
            }

            return Response({
                "total": combined
            })


        elif hasattr(user, 'is_daycare'):

            daycare_instance = day_care.objects.get(user = request.user)  # Assuming daycare is related to User

            # Consultation Appointment Report
            daycare_counts = day_care_booking.objects.filter(
                daycare=daycare_instance
            ).values('status').annotate(total=Count('id'))

            # Online Consultation Appointment Report
            def to_status_dict(queryset):
            
                data = {'accepted': 0, 'completed': 0, 'cancelled': 0}
                for entry in queryset:
                    status = entry['status'].lower()
                    if status in data:
                        data[status] += entry['total']
                return data

            # Individual breakdown
            daycare = to_status_dict(daycare_counts)

            # Total combined
            combined = {
                "accepted": daycare['accepted'] ,
                "completed": daycare['completed'] ,
                "cancelled": daycare['cancelled'] ,
            }

            return Response({
                "total": combined
            })


        elif hasattr(user, 'is_service_provider'):

            daycare_instance = service_booking.objects.get(user = request.user)  # Assuming daycare is related to User

            # Consultation Appointment Report
            daycare_counts = service_booking.objects.filter(
                daycare=daycare_instance
            ).values('status').annotate(total=Count('id'))

            # Online Consultation Appointment Report
            def to_status_dict(queryset):
            
                data = {'accepted': 0, 'completed': 0, 'cancelled': 0}
                for entry in queryset:
                    status = entry['status'].lower()
                    if status in data:
                        data[status] += entry['total']
                return data

            # Individual breakdown
            daycare = to_status_dict(daycare_counts)

            # Total combined
            combined = {
                "accepted": daycare['accepted'] ,
                "completed": daycare['completed'] ,
                "cancelled": daycare['cancelled'] ,
            }

            return Response({
                "total": combined
            })



# views.py

from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser


from .serializers import *
from .models import *
from users.permissions import *

class VendorKYCViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorKYCSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return vendor_kyc.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if vendor_kyc.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "KYC already submitted for this user."})
        serializer.save(user=self.request.user)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class accept_order(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_type = request.data.get('order_type')
        order_id = request.data.get('id')

        # Map type to model and assign field
        type_map = {
            'consultation': (consultation_appointment, 'doctor'),
            'online_consultation': (online_consultation_appointment, 'doctor'),
            'vaccination': (vaccination_appointment, 'doctor'),
            'test': (test_booking, 'doctor'),
            'service': (service_booking, 'service_provider'),
            'daycare': (day_care_booking, 'daycare'),
        }

        if order_type not in type_map:
            return Response({"detail": "Invalid order type."}, status=status.HTTP_400_BAD_REQUEST)

        model_class, assign_field = type_map[order_type]
        booking = get_object_or_404(model_class, id=order_id)

        # Check if already assigned
        if getattr(booking, assign_field):
            return Response({"detail": "Order already accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Get correct object to assign
        try:
            if assign_field == 'doctor':
                assigned_obj = user.doctor
            elif assign_field == 'service_provider':
                assigned_obj = user.service_provider
            elif assign_field == 'daycare':
                assigned_obj = user.daycare
            else:
                return Response({"detail": "User role not authorized."}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({"detail": f"User does not have {assign_field} profile."}, status=status.HTTP_403_FORBIDDEN)

        # Assign and save
        setattr(booking, assign_field, assigned_obj)
        booking.status = "accepted"
        booking.save()

        return Response({"detail": "Order accepted successfully."}, status=status.HTTP_200_OK)
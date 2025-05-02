
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.db.models import Count
# from petprofile.models import *



@login_required(login_url='login_admin')
def dashboard(request):


    operators_count = 0
    investors_count = 0
    total_money = 0


    # operators_count = operator.objects.all().count()
    # investors_count = investor.objects.all().count()

    total_money = 0
    # total_money = transactions.objects.aggregate(Sum('amount'))['amount__sum']  or 0
    



    context = {
        'operators_count' : operators_count,
        'investors_count' : investors_count,
        'total_money' : total_money
    }
    
    return render(request, 'adminDashboard.html', context)








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

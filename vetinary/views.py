
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


class all_open_bookings_doctor(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        
        # Check if the user is a doctor (adjust your logic here as necessary)
        if not hasattr(user, 'is_doctor') or not user.is_doctor:
            return Response({"detail": "Unauthorized or invalid user type"}, status=400)
        
        # Fetch data from the four tables
        consultations = consultation_appointment.objects.filter(status="open")
        online_consultations = online_consultation_appointment.objects.filter(status="open")
        vaccinations = vaccination_appointment.objects.filter(status="open")
        tests = test_booking.objects.filter(status="open")

        # Serialize the data from each table
        consultations_data = consultation_appointment_Serializer(consultations, many=True).data
        online_consultations_data = online_consultation_appointment_Serializer(online_consultations, many=True).data
        vaccinations_data = vaccination_appointment_Serializer(vaccinations, many=True).data
        tests_data = test_booking_Serializer(tests, many=True).data

        # Combine all data
        all_appointments = (
            [{"type": "consultation", **appt} for appt in consultations_data] +
            [{"type": "online_consultation", **appt} for appt in online_consultations_data] +
            [{"type": "vaccination", **appt} for appt in vaccinations_data] +
            [{"type": "test", **appt} for appt in tests_data]
        )

        # Return the combined data
        return Response({"appointments": all_appointments})


from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend



from users.permissions import *
from daycare.filters import *


class all_open_bookings_daycare(ListAPIView):
    
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsDaycare]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DayCareBookingFilter

    def get_queryset(self):
        return day_care_booking.objects.filter(status = "open").order_by('-id')
    

        


class all_open_bookings_service_provider(ListAPIView):
    
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsDaycare]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DayCareBookingFilter

    def get_queryset(self):
        return day_care_booking.objects.filter(status = "open").order_by('-id')
    

        
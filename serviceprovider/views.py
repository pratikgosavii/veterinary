from django.shortcuts import render

# Create your views here.




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class service_provider_login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if user exists and is a customer
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        print()

        if not user.is_service_provider:  # Check if `is_customer` is True
            return Response({"error": "Access denied. Not a service provider."}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"id": user.id, "email": user.email}
        }, status=status.HTTP_200_OK)


from .serializer import *
from rest_framework import generics, permissions

from rest_framework import viewsets, permissions
from .models import service_provider
from .serializer import service_provider_serializer
from rest_framework.parsers import MultiPartParser, JSONParser


from pet.models import *


from django.db.models import Count, Q

class get_services_count(APIView):

    
    def get(self, request):
        
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





from users.permissions import *

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *



class ListServiceproviderBookings(ListAPIView):
    
    serializer_class = service_provider_serializer
    permission_classes = [IsServiceProvider]
    filter_backends = [DjangoFilterBackend]
    filterset_class = service_providersFilter

    def get_queryset(self):
        return day_care_booking.objects.filter(user=self.request.user).select_related('serviceprovider').prefetch_related('pets').order_by('-id')
    


from rest_framework.exceptions import ValidationError


class ServiceProviderViewSet(viewsets.ModelViewSet):
    serializer_class = service_provider_serializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]  # ✅ Allow both JSON and form-data

    def get_queryset(self):
        return service_provider.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        
        if service_provider.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "A doctor already exists for this user."})

        serializer.save(user=self.request.user)

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

class get_service_providers(ListAPIView):
    queryset = service_provider.objects.all()
    serializer_class = service_provider_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    
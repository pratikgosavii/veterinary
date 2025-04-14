from django.shortcuts import render

# Create your views here.




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from users.permissions import *


class day_care_login(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        password = request.data.get("password")

        # Check if user exists and is a customer
        user = authenticate(mobile=mobile, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        print()

        if not user.is_daycare:  # Check if `is_customer` is True
            return Response({"error": "Access denied. Not a daycare."}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"id": user.id, "mobile": user.mobile}
        }, status=status.HTTP_200_OK)


from .serializers import *
from rest_framework import generics, permissions

class day_care_register(generics.CreateAPIView):
    
    queryset = day_care.objects.all()
    serializer_class = day_care_serializer



    
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

class get_day_care(ListAPIView):

    permission_classes = [IsCustomer]  

    queryset = day_care.objects.all()
    serializer_class = day_care_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'location']  # Example fields (update based on your model)



from rest_framework.generics import CreateAPIView, ListAPIView
from .models import day_care_booking
from .serializers import DayCareBookingSerializer
from rest_framework.permissions import IsAuthenticated



class CreateDayCareBooking(CreateAPIView):
    queryset = day_care_booking.objects.all()
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsAuthenticated]


class ListDayCareBookings(ListAPIView):
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # Or specify fields like ['date_from', 'date_to', 'payment_status']

    def get_queryset(self):
        return day_care_booking.objects.filter(user=self.request.user).distinct()
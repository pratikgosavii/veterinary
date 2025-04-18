from django.shortcuts import render

# Create your views here.




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from pet.serializers import DayCareBookingSerializer
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



class DayCareFoodMenuListView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, daycare_id):
        try:
            daycare = day_care.objects.get(id=daycare_id)
        except day_care.DoesNotExist:
            return Response({"detail": "Daycare not found."}, status=status.HTTP_404_NOT_FOUND)

        food_menus = DayCareFoodMenu.objects.filter(daycare=daycare)
        serializer = DayCareFoodMenuSerializer(food_menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ListDayCareBookings(ListAPIView):
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsDaycare]

    def get_queryset(self):
        return day_care_booking.objects.filter(user=self.request.user).select_related('daycare').prefetch_related('pets').order_by('-id')
    

    
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import day_care
from .serializers import day_care_serializer


class DayCareDetailView(RetrieveAPIView):
    queryset = day_care.objects.all()
    serializer_class = day_care_serializer
    permission_classes = [IsCustomer]
    lookup_field = 'id'  # default is 'pk', you can keep or customize this

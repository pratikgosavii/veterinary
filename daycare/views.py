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
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser


class DayCareViewSet(viewsets.ModelViewSet):

    queryset = day_care.objects.filter(is_active=True)
    serializer_class = day_care_serializer
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        user = self.request.user
        return day_care.objects.filter(user=user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"detail": "Soft deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class DayCareFoodmenuViewSet(viewsets.ModelViewSet):

    queryset = DayCareFoodMenu.objects.all()
    serializer_class = DayCareFoodMenuSerializer
    parser_classes = [JSONParser]

    def get_queryset(self):
        user = self.request.user
        return DayCareFoodMenu.objects.filter(daycare__user=user, is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        try:
            day_care_instance = day_care.objects.get(user=user, is_active=True)
        except day_care.DoesNotExist:
            raise serializers.ValidationError("Active day care not found for the user.")
        
        # Save each food menu with the correct day_care
        serializer.save(daycare=day_care_instance)

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)  # Check if data is a list (multiple food menus)
        serializer = self.get_serializer(data=request.data, many=is_many, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Handle saving each of the objects
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
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

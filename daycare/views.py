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


from .serializer import *
from rest_framework import generics, permissions

class day_care_signup(generics.CreateAPIView):
    
    queryset = day_care.objects.all()
    serializer_class = day_care_serializer



    
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

class get_day_care(ListAPIView):

    permission_classes = [IsDaycare]  

    queryset = day_care.objects.all()
    serializer_class = day_care_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'location']  # Example fields (update based on your model)

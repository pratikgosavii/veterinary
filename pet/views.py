from django.shortcuts import render

# Create your views here.





from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *

from rest_framework.generics import ListAPIView, CreateAPIView

from users.permissions import *

from django_filters.rest_framework import DjangoFilterBackend




class list_pet(ListAPIView):
    serializer_class = PetSerializer

    def get_queryset(self):
        return pet.objects.filter(owner=self.request.user)


from rest_framework.parsers import MultiPartParser, FormParser


# Add a new pet
class register_pet(CreateAPIView):
    queryset = pet.objects.all()
    serializer_class = PetSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsDaycare]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class create_pet_consultation_appointment(CreateAPIView):
    
    queryset = consultation_appointment.objects.all()
    serializer_class = consultation_appointment_Serializer
    permission_classes = [IsCustomer]



class list_pet_consultation_appointment(ListAPIView):
    serializer_class = consultation_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']  # add more as needed

    def get_queryset(self):
        return consultation_appointment.objects.filter(user=self.request.user).distinct()


class create_pet_vaccination_appointment(CreateAPIView):
    
    queryset = vaccination_appointment.objects.all()
    serializer_class = vaccination_appointment_Serializer
    permission_classes = [IsCustomer]


class list_pet_vaccination_appointment(ListAPIView):
    serializer_class = vaccination_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']  # add more as needed

    def get_queryset(self):
        return vaccination_appointment.objects.filter(user=self.request.user).distinct()

class create_pet_test_booking(CreateAPIView):
    
    queryset = test_booking.objects.all()
    serializer_class = test_booking_Serializer
    permission_classes = [IsCustomer]


class list_pet_test_booking(ListAPIView):
    serializer_class = test_booking_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']  # add more as needed

    def get_queryset(self):
        return test_booking.objects.filter(user=self.request.user).distinct()



from rest_framework.views import APIView
from rest_framework.response import Response

class CartView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        cart_items = cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            try:
                product_instance = product.objects.get(id=product_id)
            except product.DoesNotExist:
                return Response({"error": "product not found"}, status=404)

            cart_item, created = cart.objects.get_or_create(
                user=request.user,
                product=product_instance,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({"message": "Item added to cart"}, status=201)

        return Response(serializer.errors, status=400)

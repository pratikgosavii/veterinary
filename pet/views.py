from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.





from django.urls import reverse
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *

from rest_framework.generics import ListAPIView, CreateAPIView

from users.permissions import *

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action



class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsCustomer]  # Or use IsAuthenticated if needed

    def get_queryset(self):
        return pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
from datetime import date

class consultation_appointment_ViewSet(ModelViewSet):
    serializer_class = consultation_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']

    def get_queryset(self):
        return consultation_appointment.objects.filter(user=self.request.user).distinct()
    
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_appointments(self, request):
        upcoming = self.get_queryset().filter(date__gte=date.today()).order_by('date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='past')
    def past_appointments(self, request):
        past = self.get_queryset().filter(date__lt=date.today()).order_by('-date')
        serializer = self.get_serializer(past, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class online_consultation_appointment_ViewSet(ModelViewSet):
    serializer_class = online_consultation_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']

    def get_queryset(self):
        return consultation_appointment.objects.filter(user=self.request.user).distinct()
    
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_appointments(self, request):
        upcoming = self.get_queryset().filter(date__gte=date.today()).order_by('date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='past')
    def past_appointments(self, request):
        past = self.get_queryset().filter(date__lt=date.today()).order_by('-date')
        serializer = self.get_serializer(past, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class vaccination_appointment_ViewSet(ModelViewSet):
    serializer_class = vaccination_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']

    def get_queryset(self):
        return vaccination_appointment.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from rest_framework.parsers import JSONParser

class pet_test_booking_ViewSet(ModelViewSet):
    serializer_class = test_booking_Serializer
    permission_classes = [IsCustomer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']

    def get_queryset(self):
        return test_booking.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from rest_framework.views import APIView
from rest_framework.response import Response


MODEL_SERIALIZER_MAP = {
    'product': product_serializer,
    'service': service_serializer,
    'vaccination': vaccination_serializer,
    'test': test_serializer,
}


from rest_framework import status



class CartdeleteView(APIView):
    permission_classes = [IsCustomer]

    def delete(self, request, pk):
        cart_item = get_object_or_404(cart, pk=pk, user=request.user)
        cart_item.delete()
        return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)
    


class CartView(APIView):

    
    permission_classes = [IsCustomer]

    def get(self, request):
        cart_items = cart.objects.filter(user=request.user).select_related('product')
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        if isinstance(data, dict):
            data = [data]

        added = []
        failed = []

        for item in data:
            serializer = CartSerializer(data=item)
            if serializer.is_valid():
                product = serializer.validated_data['product']
                quantity = serializer.validated_data['quantity']

                cart_obj, created = cart.objects.update_or_create(
                    user=request.user,
                    product=product,
                    defaults={'quantity': quantity}
                )

                added.append({
                    "product_id": product.id,
                    "quantity": quantity,
                    "action": "created" if created else "updated"
                })
            else:
                failed.append({
                    "data": item,
                    "errors": serializer.errors
                })

        return Response({
            "message": f"{len(added)} item(s) processed.",
            "processed_items": added,
            "failed_items": failed
        }, status=status.HTTP_207_MULTI_STATUS if failed else status.HTTP_201_CREATED)
    

    
from rest_framework import generics

class create_order(generics.CreateAPIView):

    permission_classes = [IsCustomer]  

    queryset = order.objects.all()
    serializer_class = OrderSerializer



from django.contrib.auth.decorators import login_required
from .forms import *

import json
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from .models import order, order_item
from .forms import OrderForm


@login_required(login_url='login')
def update_order(request, order_id):

    order_obj = get_object_or_404(order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_obj)
        if form.is_valid():
            order_obj = form.save()
            order_obj.items.all().delete()  # clear old items

            items = json.loads(request.POST.get("items_json", "[]"))
            for i in items:
                try:
                    content_type = ContentType.objects.get(model=i['item_type'].lower())
                    content_type.model_class().objects.get(id=i['object_id'])
                except Exception as e:
                    continue

                order_item.objects.create(
                    order=order_obj,
                    content_type=content_type,
                    object_id=i['object_id'],
                    quantity=i.get('quantity', 1)
                )
            return redirect('order_success')
    else:
        form = OrderForm(instance=order_obj)

    return render(request, 'order_form.html', {'form': form})
        

@login_required(login_url='login')
def delete_order(request, order_id):

    order.objects.get(id=order_id).delete()

    return HttpResponseRedirect(reverse('list_order_admin'))


@login_required(login_url='login')
def list_order_admin(request):

    data = order.objects.prefetch_related('items__content_type').select_related('user').all()
    context = {
        'data': data
    }
    return render(request, 'list_order.html', context)




from rest_framework.permissions import IsAuthenticated


from .filters import *


class ListOrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter  # Specify the filterset class

    queryset = order.objects.all()

    def get_queryset(self):
        return order.objects.filter(user=self.request.user)


from rest_framework.generics import CreateAPIView, ListAPIView
from .models import day_care_booking
from .serializers import DayCareBookingSerializer
from rest_framework.permissions import IsAuthenticated

class CreateDayCareBooking(CreateAPIView):
    queryset = day_care_booking.objects.all()
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsCustomer]



class ListDayCareBookings(ListAPIView):
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return day_care_booking.objects.filter(user=self.request.user).select_related('daycare').prefetch_related('pets').order_by('-id')
    


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from stream_chat import StreamChat  # ✅ Correct import

import os

class GenerateStreamToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        api_key = os.getenv("STREAM_API_KEY")
        api_secret = os.getenv("STREAM_API_SECRET")

        if not api_key or not api_secret:
            return Response({"error": "Missing Stream API credentials"}, status=500)

        user_id = str(request.user.id)

        client = StreamChat(api_key=api_key, api_secret=api_secret)  # ✅
        client.upsert_user({"id": user_id, "name": request.user.username})
        token = client.create_token(user_id)

        return Response({
            "user_id": user_id,
            "token": token,
            "api_key": api_key,
        })
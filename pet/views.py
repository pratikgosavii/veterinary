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


class vaccination_appointment_ViewSet(ModelViewSet):
    serializer_class = vaccination_appointment_Serializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'date', 'payment_status']

    def get_queryset(self):
        return vaccination_appointment.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class pet_test_booking_ViewSet(ModelViewSet):
    serializer_class = test_booking_Serializer
    permission_classes = [IsCustomer]
    parser_classes = [MultiPartParser, FormParser]
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


class CartView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        cart_items = cart.objects.filter(user=request.user).select_related('content_type')  # Reduce queries
        data = []

        for item in cart_items:
            model_name = item.content_type.model
            serializer_class = MODEL_SERIALIZER_MAP.get(model_name)

            if serializer_class:
                try:
                    serialized_item = serializer_class(item.item).data
                except Exception as e:
                    serialized_item = {'error': f'Error serializing {model_name}: {str(e)}'}
            else:
                serialized_item = {'error': f'No serializer found for model: {model_name}'}

            data.append({
                'id': item.id,
                'item_type': model_name,
                'quantity': item.quantity,
                'item_data': serialized_item
            })

        return Response(data)

    def post(self, request):

        data = request.data
        if isinstance(data, dict):
            data = [data]  # Convert single item to list

        added = []
        failed = []

        for item in data:
            serializer = CartSerializer(data=item, context={'request': request})
            if serializer.is_valid():
                validated_data = serializer.validated_data
                content_type = validated_data['content_type']
                object_id = validated_data['object_id']
                quantity = validated_data['quantity']

                cart_obj, created = cart.objects.update_or_create(
                    user=request.user,
                    content_type=content_type,
                    object_id=object_id,
                    defaults={'quantity': quantity}
                )

                added.append({
                    "item_type": item["item_type"],
                    "object_id": object_id,
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

    def delete(self, request):
        
        
        data = request.data

        if isinstance(data, dict):
            data = [data]  # Convert single delete request to list

        deleted = []
        failed = []

        for item in data:
            item_type = item.get("item_type")
            object_id = item.get("object_id")

            if not item_type or not object_id:
                failed.append({
                    "data": item,
                    "error": "Both 'item_type' and 'object_id' are required."
                })
                continue

            try:
                content_type = ContentType.objects.get(model=item_type.lower())
                cart_obj = cart.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=object_id
                ).first()

                if cart_obj:
                    cart_obj.delete()
                    deleted.append({
                        "item_type": item_type,
                        "object_id": object_id
                    })
                else:
                    failed.append({
                        "data": item,
                        "error": "Cart item not found."
                    })

            except ContentType.DoesNotExist:
                failed.append({
                    "data": item,
                    "error": f"Invalid model: {item_type}"
                })

        return Response({
            "message": f"{len(deleted)} item(s) deleted.",
            "deleted_items": deleted,
            "failed_items": failed
        }, status=status.HTTP_207_MULTI_STATUS if failed else status.HTTP_200_OK)

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

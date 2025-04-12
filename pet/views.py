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
    permission_classes = [IsDaycare]  # Or use IsAuthenticated if needed

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


class CartView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        cart_items = cart.objects.filter(user=request.user)
        data = []

        for item in cart_items:
            model_name = item.content_type.model
            serializer_class = MODEL_SERIALIZER_MAP.get(model_name)

            if serializer_class:
                serialized_item = serializer_class(item.item).data
            else:
                serialized_item = {'error': f'No serializer for {model_name}'}

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
            data = [data]

        success_count = 0
        failed_items = []

        for item in data:
            serializer = AddToCartSerializer(data=item)
            if serializer.is_valid():
                validated = serializer.validated_data
                cart_item, _ = CartItem.objects.update_or_create(
                    user=request.user,
                    content_type=validated['content_type'],
                    object_id=validated['object_id'],
                    defaults={'quantity': validated['quantity']}
                )
                success_count += 1
            else:
                failed_items.append({'data': item, 'errors': serializer.errors})

        return Response({
            "message": f"{success_count} item(s) added to cart.",
            "failed_items": failed_items
        }, status=201 if success_count else 400)






from rest_framework import generics

class create_order(generics.CreateAPIView):

    permission_classes = [IsCustomer]  

    queryset = order.objects.all()
    serializer_class = OrderSerializer



from django.contrib.auth.decorators import login_required
from .forms import *

@login_required(login_url='login')
def update_order(request, order_id):

    if request.method == 'POST':

        instance = order.objects.get(id=order_id)

        forms = order_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_order_admin')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_order.html', context)
    
    else:

        instance = order.objects.get(id=order_id)
        forms = order_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_order.html', context)

        

@login_required(login_url='login')
def delete_order(request, order_id):

    order.objects.get(id=order_id).delete()

    return HttpResponseRedirect(reverse('list_order_admin'))


@login_required(login_url='login')
def list_order_admin(request):

    data = order.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_order.html', context)




from rest_framework.permissions import IsAuthenticated


class list_order(generics.ListAPIView):

   
    # queryset = order.objects.all()
    permission_classes = [IsAuthenticated, IsCustomer]  # Ensures user is logged in + is a customer
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


    def get_queryset(self):
        
        print(self.request.user)
        print(order.objects.all().values('user'))

        return order.objects.filter(user=self.request.user)
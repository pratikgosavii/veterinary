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


from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
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
        return consultation_appointment.objects.filter(user=self.request.user).order_by('date')
    
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
        return online_consultation_appointment.objects.filter(user=self.request.user).distinct()
    
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

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_bookings(self, request):
        today = date.today()
        upcoming = self.get_queryset().filter(date__date__gte=today).order_by('date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='past')
    def past_bookings(self, request):
        today = date.today()
        past = self.get_queryset().filter(date__date__lt=today).order_by('-date')
        serializer = self.get_serializer(past, many=True)
        return Response(serializer.data)


class past_vaccination_ViewSet(ModelViewSet):
    
    serializer_class = PastVaccinationSerializer
    permission_classes = [IsCustomer]
    parser_classes = [MultiPartParser, FormParser]  # For file uploads

    def get_queryset(self):
        return pet_vaccination.objects.filter()

    def perform_create(self, serializer):
        serializer.save()


    def get_queryset(self):
        pet_id = self.request.query_params.get('pet_id')
        
        if pet_id:
            return pet_vaccination.objects.filter(pet__id=pet_id, pet__owner=self.request.user)
        
        return pet_vaccination.objects.none()  # Or all() if you want default behavior

from rest_framework.views import APIView
from rest_framework.response import Response


MODEL_SERIALIZER_MAP = {
    'product': product_serializer,
    'service': service_serializer,
    'vaccination': vaccination_serializer,
    'test': test_serializer,
}


from rest_framework import status

class pet_services_booking_ViewSet(ModelViewSet):
    serializer_class = service_booking_Serializer
    permission_classes = [IsCustomer]  # Or [IsAuthenticated] based on your setup
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_status', 'date']

    def get_queryset(self):
        return service_booking.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_bookings(self, request):
        upcoming = self.get_queryset().filter(date__gte=datetime.now()).order_by('date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='past')
    def past_bookings(self, request):
        past = self.get_queryset().filter(date__lt=datetime.now()).order_by('-date')
        serializer = self.get_serializer(past, many=True)
        return Response(serializer.data)



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

    order_obj = get_object_or_404(order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_obj)
        if form.is_valid():

            form.save()
            
            return redirect('list_order_admin')

        else:

            print(form.errors)

            return render(request, 'add_order.html', {'form': form})

    else:
        form = OrderForm(instance=order_obj)

        return render(request, 'add_order.html', {'form': form})
        

@login_required(login_url='login')
def delete_order(request, order_id):

    order.objects.get(id=order_id).delete()

    return HttpResponseRedirect(reverse('list_order_admin'))


@login_required(login_url='login')
def list_order_admin(request):

    data = order.objects.all().order_by('-id')
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




class get_prescription(generics.ListAPIView):

    from doctor.serializer import PrescriptionSerializer
    from doctor.models import Prescription

    serializer_class = PrescriptionSerializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        appoinment_id = self.request.query_params.get('appoinment_id')

        return Prescription.objects.filter(consultation__user=self.request.user, consultation__id = appoinment_id)


from rest_framework.generics import CreateAPIView, ListAPIView
from .models import day_care_booking
from .serializers import DayCareBookingSerializer
from rest_framework.permissions import IsAuthenticated

class CreateDayCareBooking(CreateAPIView):
    queryset = day_care_booking.objects.all()
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsCustomer]


from rest_framework.generics import RetrieveAPIView

class DayCareBookingDetailView(RetrieveAPIView):
    queryset = day_care_booking.objects.all()
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsCustomer]


class ListDayCareBookings(generics.ListAPIView):
    serializer_class = DayCareBookingSerializer
    permission_classes = [IsCustomer]


    def get_queryset(self):
        print('=----------------')
        print('=----------------')
        print('=----------------')
        print(self.request.user)
        return day_care_booking.objects.filter(user=self.request.user).order_by('-id')
    



from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.permissions import *


@api_view(['GET'])
@permission_classes([IsCustomer])  # Your custom permission to ensure user is a customer
def customer_booking_detail_view(request, type, id):
    user = request.user

    model_map = {
        "consultation": (consultation_appointment, consultation_appointment_Serializer, "user"),
        "online_consultation": (online_consultation_appointment, online_consultation_appointment_Serializer, "user"),
        "vaccination": (vaccination_appointment, vaccination_appointment_Serializer, "user"),
        "test": (test_booking, test_booking_Serializer, "user"),
        "daycare": (day_care_booking, DayCareBookingSerializer, "user"),
        "service": (service_booking, service_booking_Serializer, "user"),
    }

    if type not in model_map:
        return Response({"detail": "Invalid type"}, status=400)

    model_class, serializer_class, user_field = model_map[type]

    # Filter the booking by the customer user
    # Assuming each booking model has a foreign key field to the customer (e.g. 'customer')
    # and Customer has a OneToOne or ForeignKey relation to User

    try:
        # Get the booking instance with matching id and customer user
        instance = model_class.objects.get(pk=id, **{user_field: user})
    except model_class.DoesNotExist:
        return Response({"detail": "Booking not found or you don't have permission"}, status=404)

    serializer = serializer_class(instance)
    return Response(serializer.data)




from doctor.serializer import *

class ConsultationReportListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        appointment_ids = consultation_appointment.objects.filter(user=user).values_list('id', flat=True)
        reports = ConsultationAppointmentReport.objects.filter(appointment_id__in=appointment_ids)
        serializer = ConsultationAppointmentReportSerializer(reports, many=True)
        return Response(serializer.data)

# ✅ 2. Get Online Consultation Reports
class OnlineConsultationReportListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        appointment_ids = online_consultation_appointment.objects.filter(user=user).values_list('id', flat=True)
        reports = OnlineConsultationAppointmentReport.objects.filter(appointment_id__in=appointment_ids)
        serializer = OnlineConsultationAppointmentReportSerializer(reports, many=True)
        return Response(serializer.data)

# ✅ 3. Get Test Booking Reports
class TestBookingReportListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        booking_ids = test_booking.objects.filter(user=user).values_list('id', flat=True)
        reports = TestBookingReport.objects.filter(booking_id__in=booking_ids)
        serializer = TestBookingReportSerializer(reports, many=True)
        return Response(serializer.data)
    


from rest_framework import viewsets
from itertools import chain
from django.utils import timezone
from datetime.utils import datetime, time
from django.utils.timezone import make_aware, is_naive


class AllAppointmentsViewSet(viewsets.ViewSet):
    
    permission_classes = [IsCustomer]

    def list(self, request):
        user = request.user
        now = timezone.now()

        # Fetch all types of appointments for the user
        consultations = consultation_appointment.objects.filter(user=user)
        online_consultations = online_consultation_appointment.objects.filter(user=user)
        vaccinations = vaccination_appointment.objects.filter(user=user)
        tests = test_booking.objects.filter(user=user)
        daycares = day_care_booking.objects.filter(user=user)
        services = service_booking.objects.filter(user=user)

        # Combine and annotate with type
        all_appointments = list(chain(
            [("consultation", appt) for appt in consultations],
            [("online_consultation", appt) for appt in online_consultations],
            [("vaccination", appt) for appt in vaccinations],
            [("test", appt) for appt in tests],
            [("daycare", appt) for appt in daycares],
            [("service", appt) for appt in services],
        ))

        upcoming = []
        past = []

        def normalize_date(appt):
            raw_date = getattr(appt, 'date_from', getattr(appt, 'date', None))
            if isinstance(raw_date, datetime):
                dt = raw_date
            elif isinstance(raw_date, date):
                dt = datetime.combine(raw_date, time.min)
            else:
                return None
            return make_aware(dt) if is_naive(dt) else dt

        for appt_type, appt in all_appointments:
            appt_datetime = normalize_date(appt)
            if not appt_datetime:
                continue
            if appt_datetime >= now:
                upcoming.append((appt_type, appt, appt_datetime))
            else:
                past.append((appt_type, appt, appt_datetime))

        def serialize(appt_type, appt):
            serializers_map = {
                "consultation": consultation_appointment_Serializer,
                "online_consultation": online_consultation_appointment_Serializer,
                "vaccination": vaccination_appointment_Serializer,
                "test": test_booking_Serializer,
                "daycare": DayCareBookingSerializer,
                "service": service_booking_Serializer,
            }
            serializer_class = serializers_map[appt_type]
            return {
                "type": appt_type,
                "data": serializer_class(appt, context={"request": request}).data
            }

        return Response({
            "upcoming": [serialize(t, a) for t, a, _ in sorted(upcoming, key=lambda x: x[2])],
            "past": [serialize(t, a) for t, a, _ in sorted(past, key=lambda x: x[2], reverse=True)],
        })


class AllConsultationReportsAPIView(APIView):

    def get(self, request):
        consultation_reports = ConsultationAppointmentReport.objects.filter(appointment__user=request.user)
        online_reports = OnlineConsultationAppointmentReport.objects.filter(appointment__user=request.user)

        consultation_serialized = ConsultationAppointmentReportSerializer(consultation_reports, many=True).data
        online_serialized = OnlineConsultationAppointmentReportSerializer(online_reports, many=True).data

        # Add type field to distinguish
        for report in consultation_serialized:
            report["type"] = "consultation"
        for report in online_serialized:
            report["type"] = "online_consultation"

        combined = consultation_serialized + online_serialized
        return Response(combined, status=status.HTTP_200_OK)




# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from stream_chat import StreamChat  # ✅ Correct import

import os



class GenerateStreamToken(APIView):

    def get(self, request):
        api_key = os.getenv("STREAM_API_KEY")
        api_secret = os.getenv("STREAM_API_SECRET")

        print("✅ STREAM_API_KEY from .env:", os.getenv("STREAM_API_KEY"))

        if not api_key or not api_secret:
            return Response({"error": "Missing Stream API credentials"}, status=500)

        user_id = request.GET.get("user_id")


        client = StreamChat(api_key=api_key, api_secret=api_secret)  # ✅
        client.upsert_user({"id": user_id, "name": request.user.username})
        token = client.create_token(user_id)

        return Response({
            "user_id": user_id,
            "token": token,
            "api_key": api_key,
        })


from rest_framework.views import APIView
from rest_framework.response import Response
import os
import uuid



class GenerateOrJoinCall(APIView):
    def get(self, request):
        api_key = os.getenv("STREAM_API_KEY")
        api_secret = os.getenv("STREAM_API_SECRET")
        user_id = str(request.user.id)
        appoinment_id = request.GET.get("appoinment_id")
        call_id = request.GET.get("call_id") or str(uuid.uuid4())

        if not api_key or not api_secret or not user_id or not appoinment_id:
            return Response({"error": "Missing required params"}, status=400)

        try:
            appointment = online_consultation_appointment.objects.get(id=appoinment_id)
        except online_consultation_appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=404)

        doctor = appointment.doctor

        client = StreamChat(api_key=api_key, api_secret=api_secret)
        client.upsert_user({"id": user_id})
        token = client.create_token(user_id)

        # Save to Apoinments_video_details
        Apoinments_video_details.objects.create(
            appoinment_id=appointment.id,
            call_id=call_id,
            token=token,  # If token is string, update model field to CharField
            doctor=doctor
        )


        return Response({
            "user_id": user_id,
            "token": token,
            "api_key": api_key,
            "call_id": call_id
        })
    



def OnlineConsultationUpdateView(request, instance_id):

    instance = online_consultation_appointment.objects.get(id = instance_id)
    forms = OnlineConsultationAppointmentForm(instance = instance, user=request.user)

    if request.method == "POST":

        forms = OnlineConsultationAppointmentForm(request.POST, request.FILES, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('admin_all_booking')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'online_consultation.html', context)
    else:
        return render(request, 'online_consultation.html', { 'form' : forms})

def OnlineConsultationDeleteView(request, instance_id):

    online_consultation_appointment.objects.get(id = instance_id).delete()

    return redirect('admin_all_booking')



def ConsultationUpdateView(request, instance_id):

    instance = consultation_appointment.objects.get(id = instance_id)
    forms = ConsultationAppointmentForm(instance = instance, user=request.user)

    if request.method == "POST":

        forms = ConsultationAppointmentForm(request.POST, request.FILES, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('admin_all_booking')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'consultation.html', context)
    else:
        return render(request, 'consultation.html', { 'form' : forms})
    
def ConsultationDeleteView(request, instance_id):

    consultation_appointment.objects.get(id = instance_id).delete()

    return redirect('admin_all_booking')




def VaccinationUpdateView(request, instance_id):

    instance = vaccination_appointment.objects.get(id = instance_id)
    forms = VaccinationAppointmentForm(instance = instance, user=request.user)

    if request.method == "POST":

        forms = VaccinationAppointmentForm(request.POST, request.FILES, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('admin_all_booking')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'vaccination_booking.html', context)
    else:
        return render(request, 'vaccination_booking.html', { 'form' : forms})


def VaccinationDeleteView(request, instance_id):

    vaccination_appointment.objects.get(id = instance_id).delete()

    return redirect('admin_all_booking')



def TestBookingUpdateView(request, instance_id):

    instance = test_booking.objects.get(id = instance_id)
    forms = TestBookingForm(instance = instance, user=request.user)

    if request.method == "POST":

        forms = TestBookingForm(request.POST, request.FILES, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('admin_all_booking')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'test_boking.html', context)
    else:
        return render(request, 'test_booking.html', { 'form' : forms})


def TestBookingDeleteView(request, instance_id):

    test_booking.objects.get(id = instance_id).delete()

    return redirect('admin_all_booking')



def DayCareUpdateView(request, instance_id):

    instance = day_care_booking.objects.get(id = instance_id)
    forms = DayCareBookingForm(instance = instance, user=request.user)

    if request.method == "POST":

        forms = DayCareBookingForm(request.POST, request.FILES, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('admin_all_booking')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'dayCare_booking.html', context)
    else:
        return render(request, 'dayCare_booking.html', { 'form' : forms})


def DayCareDeleteView(request, instance_id):

    day_care_booking.objects.get(id = instance_id).delete()

    return redirect('admin_all_booking')




def ServiceBookingUpdateView(request, instance_id):

    instance = service_booking.objects.get(id = instance_id)
    forms = ServiceBookingForm(instance = instance, user=request.user)

    if request.method == "POST":

        forms = ServiceBookingForm(request.POST, request.FILES, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('admin_all_booking')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'service_booking.html', context)
    else:
        return render(request, 'service_booking.html', { 'form' : forms})


def ServiceBookingDeleteView(request, instance_id):

    service_booking.objects.get(id = instance_id).delete()

    return redirect('admin_all_booking')




from rest_framework import viewsets, permissions


class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





class TicketMessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        ticket_id = request.query_params.get('ticket_id')
        if not ticket_id:
            return Response({'error': 'ticket_id is required'}, status=400)

        messages = TicketMessage.objects.filter(ticket__id=ticket_id).order_by('created_at')
        serializer = TicketMessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        ticket_id = request.data.get('ticket')
        message = request.data.get('message')

        if not ticket_id or not message:
            return Response({'error': 'ticket and message are required'}, status=400)

        ticket = get_object_or_404(SupportTicket, id=ticket_id)

        new_message = TicketMessage.objects.create(
            ticket=ticket,
            sender=request.user,
            message=message
        )

        serializer = TicketMessageSerializer(new_message, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

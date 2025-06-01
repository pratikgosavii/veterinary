
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.db.models import Count
# from petprofile.models import *




from django.urls import reverse
from rest_framework.response import Response
from rest_framework import viewsets
from itertools import chain
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware, is_naive
from rest_framework.generics import CreateAPIView, ListAPIView
from pet.serializers import *
from doctor.serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from itertools import chain
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware, is_naive


class all_open_bookings(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        appointments = []

        def serialize(qs, appt_type):
            return [
                {
                    "id": obj.id,
                    "type": appt_type,
                    "status": obj.status,
                    "date": str(getattr(obj, "date", None)),  # Adjust as needed
                    "amount": getattr(obj, "amount", getattr(obj, "total_amount", None)),
                    "name": obj.user.first_name + obj.user.last_name,  # Adjust as needed
                }
                for obj in qs
            ]

        if user.is_doctor:

            print('---------1-------------------')
            online_consultations = online_consultation_appointment.objects.filter(status="open")
            vaccinations = vaccination_appointment.objects.filter(status="open")
            tests = test_booking.objects.filter(status="open")

            appointments = (
                serialize(online_consultations, "online_consultation") +
                serialize(vaccinations, "vaccination") +
                serialize(tests, "test")
            )

        elif user.is_daycare:
            print('---------2-------------------')

            daycares = day_care_booking.objects.filter(status="open")
            appointments = serialize(daycares, "daycare")

        elif user.is_service_provider:
            print('---------3-------------------')

            services = service_booking.objects.filter(status="open")
            appointments = serialize(services, "service")

        else:
            return Response({"detail": "Invalid user type"}, status=400)

        return Response({"appointments": appointments})
    

from datetime import date, datetime

class all_vendor_bookings(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        today = date.today()

        upcoming_appointments = []
        past_appointments = []

        def serialize(qs, appt_type):
            return [
                {
                    "id": obj.id,
                    "type": appt_type,
                    "status": obj.status,
                    "date": obj.date,
                    "amount": getattr(obj, "amount", getattr(obj, "total_amount", None)),
                    "name": f"{obj.user.first_name} {obj.user.last_name}",
                }
                for obj in qs
            ]

        all_appointments = []

        if user.is_doctor:
            print('----------------1-----------------')
            doctor_instance = doctor.objects.get(user=user)
            all_appointments += (
                serialize(online_consultation_appointment.objects.filter(doctor=doctor_instance), "online_consultation") +
                serialize(consultation_appointment.objects.filter(doctor=doctor_instance), "consultation") +
                serialize(vaccination_appointment.objects.filter(doctor=doctor_instance), "vaccination") +
                serialize(test_booking.objects.filter(doctor=doctor_instance), "test")
            )


        elif user.is_daycare:
            print('----------------2-----------------')

            daycare_instance = day_care.objects.get(user=user)
            all_appointments += serialize(day_care_booking.objects.filter(daycare=daycare_instance), "daycare")

        elif user.is_service_provider:
            print('----------------3-----------------')

            service_provider_instance = service_provider.objects.get(user=user)
            all_appointments += serialize(service_booking.objects.filter(service_provider=service_provider_instance), "service")

        else:
            return Response({"detail": "Invalid user type"}, status=400)

        for appt in all_appointments:
            appt_date = appt["date"]
           
            if appt_date and appt_date.date() >= today:
                print('------------------------')
                upcoming_appointments.append(appt)
            else:
                past_appointments.append(appt)

        return Response({
            "upcoming": upcoming_appointments,
            "past": past_appointments
        })
    


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.permissions import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_booking_detail_view(request, type, id):
    user = request.user

    # Map type to model and serializer
    model_map = {
        "consultation": (consultation_appointment, consultation_appointment_Serializer),
        "online_consultation": (online_consultation_appointment, online_consultation_appointment_Serializer),
        "vaccination": (vaccination_appointment, vaccination_appointment_Serializer),
        "test": (test_booking, test_booking_Serializer),
        "daycare": (day_care_booking, DayCareBookingSerializer),
        "service": (service_booking, service_booking_Serializer),
    }

    if type not in model_map:
        return Response({"detail": "Invalid type"}, status=400)

    model_class, serializer_class = model_map[type]

    # Filter logic based on user type
    if type in ["consultation", "online_consultation", "vaccination", "test"]:
        if not user.is_doctor:
            return Response({"detail": "Unauthorized"}, status=403)
        doctor_instance = doctor.objects.get(user=user)
        instance = model_class.objects.filter(pk=id, doctor=doctor_instance).first()

    elif type == "daycare":
        if not user.is_daycare:
            return Response({"detail": "Unauthorized"}, status=403)
        daycare_instance = day_care.objects.get(user=user)
        instance = model_class.objects.filter(pk=id, daycare=daycare_instance).first()

    elif type == "service":
        if not user.is_service_provider:
            return Response({"detail": "Unauthorized"}, status=403)
        service_instance = service_provider.objects.get(user=user)
        instance = model_class.objects.filter(pk=id, service_provider=service_instance).first()

    else:
        instance = None

    if not instance:
        return Response({"detail": "Booking not found"}, status=404)

    serializer = serializer_class(instance)
    return Response(serializer.data)




class all_bookings_count(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        

        user = request.user
        

        if user.is_doctor:

        
            doctor_instance = doctor.objects.get(user = request.user)  # Assuming doctor is related to User

            # Consultation Appointment Report
            consultation_counts = consultation_appointment.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))

            # Online Consultation Appointment Report
            online_counts = online_consultation_appointment.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))

            # Test Booking Report
            vaccination_counts = vaccination_appointment.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))


            # Test Booking Report
            test_counts = test_booking.objects.filter(
                doctor=doctor_instance
            ).values('status').annotate(total=Count('id'))

            def to_status_dict(queryset):
                data = {'accepted': 0, 'completed': 0, 'cancelled': 0}
                for entry in queryset:
                    status = entry['status'].lower()
                    if status in data:
                        data[status] += entry['total']
                return data

            # Individual breakdown
            consultation = to_status_dict(consultation_counts)
            online = to_status_dict(online_counts)
            test = to_status_dict(test_counts)
            vaccination = to_status_dict(vaccination_counts)

            # Total combined
            combined = {
                "accepted": consultation['accepted'] + online['accepted'] + test['accepted'] + vaccination['accepted'],
                "completed": consultation['completed'] + online['completed'] + test['completed'] + vaccination['completed'],
                "cancelled": consultation['cancelled'] + online['cancelled'] + test['cancelled'] + vaccination['cancelled'] ,
            }

            return Response({
                "total": combined
            })


        elif user.is_daycare:

            daycare_instance = day_care.objects.get(user = request.user)  # Assuming daycare is related to User

            # Consultation Appointment Report
            daycare_counts = day_care_booking.objects.filter(
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


        elif user.is_service_provider:

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



# views.py

from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser


from .serializers import *
from .models import *
from users.permissions import *

class VendorKYCViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorKYCSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        return vendor_kyc.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if vendor_kyc.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "KYC already submitted for this user."})
        serializer.save(user=self.request.user)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class accept_order(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_type = request.data.get('order_type')
        order_id = request.data.get('order_id')

        # Map type to model and assign field
        type_map = {
            'consultation': (consultation_appointment, 'doctor'),
            'online_consultation': (online_consultation_appointment, 'doctor'),
            'vaccination': (vaccination_appointment, 'doctor'),
            'test': (test_booking, 'doctor'),
            'service': (service_booking, 'service_provider'),
            'daycare': (day_care_booking, 'daycare'),
        }

        if order_type not in type_map:
            return Response({"detail": "Invalid order type."}, status=status.HTTP_400_BAD_REQUEST)

        model_class, assign_field = type_map[order_type]

        print(model_class)
        print(order_id)
        booking = get_object_or_404(model_class, id=order_id)

        # Check if already assigned
        if getattr(booking, assign_field):
            return Response({"detail": "Order already accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # Get correct object to assign
        try:
            if assign_field == 'doctor':
                assigned_obj = user.doctor
            elif assign_field == 'service_provider':
                assigned_obj = user.service_provider
            elif assign_field == 'daycare':
                assigned_obj = user.daycare
            else:
                return Response({"detail": "User role not authorized."}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({"detail": f"User does not have {assign_field} profile."}, status=status.HTTP_403_FORBIDDEN)

        # Assign and save
        setattr(booking, assign_field, assigned_obj)
        booking.status = "accepted"
        booking.save()

        return Response({"detail": "Order accepted successfully."}, status=status.HTTP_200_OK)



from django.utils import timezone


class serviceHistoryViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        now = timezone.now()
        all_appointments = []

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

        if user.is_doctor:
            consultations = consultation_appointment.objects.filter(
                doctor=user.doctor, status="completed", date__lt=now
            )
            online_consultations = online_consultation_appointment.objects.filter(
                doctor=user.doctor, status="completed", date__lt=now
            )
            vaccinations = vaccination_appointment.objects.filter(
                doctor=user.doctor, status="completed", date__lt=now
            )
            tests = test_booking.objects.filter(
                doctor=user.doctor, status="completed", date__lt=now
            )

            all_appointments = list(chain(
                [("consultation", appt) for appt in consultations],
                [("online_consultation", appt) for appt in online_consultations],
                [("vaccination", appt) for appt in vaccinations],
                [("test", appt) for appt in tests],
            ))

        elif user.is_daycare:
            daycares = day_care_booking.objects.filter(
                daycare=user.day_care, status="completed", date_from__lt=now
            )
            all_appointments = [("daycare", appt) for appt in daycares]

        elif user.is_service_provider:
            services = service_booking.objects.filter(
                service_provider=user.service_provider, status="completed", date__lt=now
            )
            all_appointments = [("service", appt) for appt in services]

        else:
            return Response({"detail": "Invalid user type"}, status=400)

        return Response({
            "past_completed": [serialize(t, a) for t, a in all_appointments]
        })
    





def kyc_list(request):

    data = vendor_kyc.objects.all()

    return render(request, 'vendor_kyc_list.html', { 'data' : data})


from .forms import *

def update_kyc(request, kyc_id):

    instance = vendor_kyc.objects.get(id = kyc_id)

    if request.method == 'POST':


        approved = request.POST.get("approved") == "on"
        
        if approved:
            instance.approved = True
            instance.save()
            return redirect('kyc_list')


        else:
            return redirect('kyc_list')
    
    else:

        forms = vendor_kyc_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'update_kyc.html', context)




from django.utils.dateparse import parse_datetime


def admin_all_booking(request):
    status_filter = request.GET.get("status")
    user_filter = request.GET.get("user")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    def serialize(qs, appt_type):
        data = []
        for obj in qs:
            # Apply filters
            if status_filter and obj.status != status_filter:
                continue

            if user_filter and str(obj.user.id) != user_filter:
                continue

            if date_from and getattr(obj, "date", None):
                dt = parse_datetime(date_from)
                if dt is not None:
                    dt = make_aware(dt)
                    if obj.date < dt:
                        continue


            if date_to and getattr(obj, "date", None):
                dt = parse_datetime(date_to)
                if dt is not None:
                    dt = make_aware(dt)
                    if obj.date > dt:
                        continue


            # Provider logic
            provider_user = None
            if hasattr(obj, 'doctor') and obj.doctor:
                provider_user = obj.doctor.user
            elif hasattr(obj, 'service_provider') and obj.service_provider:
                provider_user = obj.service_provider.user

            # Fallback location
            location = ""
            if hasattr(obj, 'address') and obj.address:
                location = str(obj.address)

            url_update_name = f"{appt_type.lower().replace(' ', '_')}_update"
            url_delete_name = f"{appt_type.lower().replace(' ', '_')}_delete"

            try:
                url_update = reverse(url_update_name, args=[obj.id])
            except:
                url_update = "#"

            try:
                url_delete = reverse(url_delete_name, args=[obj.id])
            except:
                url_delete = "#"

            data.append({
                "id": obj.id,
                "type": appt_type,
                "status": obj.status,
                "date": getattr(obj, "date", None),
                "amount": getattr(obj, "amount", getattr(obj, "total_cost", None)),
                "name": f"{obj.user.first_name} {obj.user.last_name}",
                "provider_type": appt_type,
                "provider_name": f"{provider_user.first_name} {provider_user.last_name}" if provider_user else "N/A",
                "location": location,
                "booking_id": obj.booking_id,
                "url_update": url_update,
                "url_delete": url_delete,
            })
        return data

    appointments = []
    appointments += serialize(consultation_appointment.objects.all(), "Consultation")
    appointments += serialize(online_consultation_appointment.objects.all(), "Online Consultation")
    appointments += serialize(vaccination_appointment.objects.all(), "Vaccination")
    appointments += serialize(test_booking.objects.all(), "Test")
    appointments += serialize(day_care_booking.objects.all(), "Daycare")
    appointments += serialize(service_booking.objects.all(), "Service")

    return render(request, "admin_all_booking.html", {
        "appointments": appointments,
    })



def admin_all_open_booking(request):

    def serialize(qs, appt_type):
        data = []
        for obj in qs:
            # Determine provider (doctor or service provider)
            provider_user = None
            if hasattr(obj, 'doctor') and obj.doctor:
                provider_user = obj.doctor.user
            elif hasattr(obj, 'service_provider') and obj.service_provider:
                provider_user = obj.service_provider.user

            # Fallback location or address field
            location = ""
            if hasattr(obj, 'address') and obj.address:
                location = str(obj.address)

            data.append({
                "id": obj.id,
                "type": appt_type,
                "status": obj.status,
                "date": getattr(obj, "date", None),
                "amount": getattr(obj, "amount", getattr(obj, "total_cost", None)),
                "name": f"{obj.user.first_name} {obj.user.last_name}",
                "provider_type": appt_type,
                "provider_name": f"{provider_user.first_name} {provider_user.last_name}" if provider_user else "N/A",
                "location": location,
            })
        return data

    appointments = []

    appointments += serialize(online_consultation_appointment.objects.filter(status="open"), "Online Consultation")
    appointments += serialize(vaccination_appointment.objects.filter(status="open"), "Vaccination")
    appointments += serialize(test_booking.objects.filter(status="open"), "Test")
    appointments += serialize(day_care_booking.objects.filter(status="open"), "Daycare")
    appointments += serialize(service_booking.objects.filter(status="open"), "Service")


    return render(request, "all_open_appoinment.html", {"appointments": appointments})


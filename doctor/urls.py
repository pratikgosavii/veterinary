from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('Prescription', PrescriptionViewSet, basename='PrescriptionViewSet')

urlpatterns = [

    path('get-doctor/', get_doctor.as_view(), name='get_doctor'),
    path('get-appointment/', get_doctor.as_view(), name='get_doctor'),

    path('get-appointment-count/', get_appointment_count.as_view(), name='get_appointment_count'),

    path('list-consultation-appointment/', list_consultation_appointment.as_view(), name='list_consultation_appointment'),
    path('list-vaccination-appointment/', list_vaccination_appointment.as_view(), name='list_vaccination_appointment'),

    path('list-test-booking/', list_test_booking.as_view(), name='list_test_booking'),
  
    path('consultation-reports/', ConsultationReportView.as_view()),
    path('online-consultation-reports/', OnlineConsultationReportView.as_view()),
    path('test-reports/', TestReportView.as_view()),
    path('vaccination-reports/', VaccinationReportView.as_view()),
    
    path('appointment-video-list/', appointment_video_list.as_view()),



] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
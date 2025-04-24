from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctor')

urlpatterns = [



    # path('add-doctor/', add_doctor, name='add_doctor'),
    # path('update-doctor/<int:doctor_id>/', update_doctor, name='update_doctor'),
    # path('list-doctor/', list_doctor, name='list_doctor'),
    # path('delete-doctor/<int:doctor_id>/', delete_doctor, name='delete_doctor'),
    path('get-doctor/', get_doctor.as_view(), name='get_doctor'),

    # path('login-doctor/', doctor_login.as_view(), name='login_doctor'),
    # path('signup-doctor/', doctor_signup.as_view(), name='signup_doctor'),

    path('list-consultation-appointment/', list_consultation_appointment.as_view(), name='list_consultation_appointment'),
    path('list-vaccination-appointment/', list_vaccination_appointment.as_view(), name='list_vaccination_appointment'),

    path('list-test-booking/', list_test_booking.as_view(), name='list_test_booking'),
  
    path('consultation-reports/', ConsultationReportView.as_view()),
    path('online-consultation-reports/', OnlineConsultationReportView.as_view()),
    path('test-reports/', TestReportView.as_view()),



] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static


from rest_framework.routers import DefaultRouter
from .views import pet_test_booking_ViewSet

router = DefaultRouter()
router.register(r'pet-test-booking', pet_test_booking_ViewSet, basename='pet-test-booking')
router.register(r'pet-vaccination-appointment', vaccination_appointment_ViewSet, basename='pet-vaccination-appointment')
router.register(r'pet-consultation-appointment', consultation_appointment_ViewSet, basename='pet-consultation-appointment')
router.register(r'pet-online-consultation-appointment', online_consultation_appointment_ViewSet, basename='pet-online-consultation-appointment')
router.register(r'pet-services-booking', pet_services_booking_ViewSet, basename='pet-services-booking')
router.register(r'pet', PetViewSet, basename='pet')


urlpatterns = [

    path('book-daycare/', CreateDayCareBooking.as_view(), name='book_daycare'),

    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartdeleteView.as_view(), name='cart'),
    
    path('create-order/', create_order.as_view(), name='create_order'),
    path('update-order/<order_id>', update_order, name='update_order'),
    path('list-order-admin/', list_order_admin, name='list_order_admin'),
    path('delete-order/<order_id>', delete_order, name='delete_order'),
    path('get-order/', ListOrderView.as_view(), name='list_order'),

    path('reports/consultation/', ConsultationReportListView.as_view()),
    path('reports/online-consultation/', OnlineConsultationReportListView.as_view()),
    path('reports/test-booking/', TestBookingReportListView.as_view()),
    path('all-consultation-reports/', AllConsultationReportsAPIView.as_view()),

    path("stream/token/", GenerateStreamToken.as_view()),

    path('list-day-care-bookings/', ListDayCareBookings.as_view(), name='list_daycare_bookings'),

] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
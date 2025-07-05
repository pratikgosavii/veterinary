from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static


from rest_framework.routers import DefaultRouter
from .views import pet_test_booking_ViewSet

router = DefaultRouter()
router.register(r'pet-test-booking', pet_test_booking_ViewSet, basename='pet-test-booking')
router.register(r'pet-past-vaccination', past_vaccination_ViewSet, basename='past_vaccination_ViewSet')
router.register(r'pet-vaccination-appointment', vaccination_appointment_ViewSet, basename='pet-vaccination-appointment')
router.register(r'pet-consultation-appointment', consultation_appointment_ViewSet, basename='pet-consultation-appointment')
router.register(r'pet-online-consultation-appointment', online_consultation_appointment_ViewSet, basename='pet-online-consultation-appointment')
router.register(r'pet-services-booking', pet_services_booking_ViewSet, basename='pet-services-booking')
router.register(r'pet', PetViewSet, basename='pet')
router.register(r'all-appointments', AllAppointmentsViewSet, basename='all-appointments')

router.register('tickets', SupportTicketViewSet, basename='tickets')
router.register('ticket-messages', TicketMessageViewSet, basename='ticket-messages')


urlpatterns = [

    path('book-daycare/', CreateDayCareBooking.as_view(), name='book_daycare'),
    path('retrive-booking-daycare/<int:pk>/', DayCareBookingDetailView.as_view(), name='DayCareBookingDetailView'),
    path('list-day-care-bookings/', ListDayCareBookings.as_view(), name='list_daycare_bookings'),

    path('customer-booking-detail/<str:type>/<int:id>/', customer_booking_detail_view, name='customer-booking-detail'),


    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', CartdeleteView.as_view(), name='cart'),
    
    path('create-order/', create_order.as_view(), name='create_order'),
    path('update-order/<order_id>', update_order, name='update_order'),
    path('list-order-admin/', list_order_admin, name='list_order_admin'),
    path('delete-order/<order_id>', delete_order, name='delete_order'),
    path('get-order/', ListOrderView.as_view(), name='list_order'),


    path('online_consultation/update/<instance_id>', OnlineConsultationUpdateView, name='online_consultation_update'),
    path('online_consultation/<instance_id>', OnlineConsultationDeleteView, name='online_consultation_delete'),

    path('consultation/update/<instance_id>', ConsultationUpdateView, name='consultation_update'),
    path('consultation/<instance_id>', ConsultationDeleteView, name='consultation_delete'),

    path('vaccination/<instance_id>', VaccinationUpdateView, name='vaccination_update'),
    path('vaccination/<instance_id>', VaccinationDeleteView, name='vaccination_delete'),

    path('test/<instance_id>', TestBookingUpdateView, name='test_update'),
    path('test/<instance_id>', TestBookingDeleteView, name='test_delete'),

    path('daycare/<instance_id>', DayCareUpdateView, name='daycare_update'),
    path('daycare/<instance_id>', DayCareDeleteView, name='daycare_delete'),

    path('service/<instance_id>', ServiceBookingUpdateView, name='service_update'),
    path('service/<instance_id>', ServiceBookingDeleteView, name='service_delete'),


    path('reports/consultation/', ConsultationReportListView.as_view()),
    path('reports/online-consultation/', OnlineConsultationReportListView.as_view()),
    path('reports/test-booking/', TestBookingReportListView.as_view()),
    path('all-consultation-reports/', AllConsultationReportsAPIView.as_view()),

    path("stream/token/", GenerateStreamToken.as_view()),
    path("stream/generateforvideo/", GenerateOrJoinCall.as_view()),


] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
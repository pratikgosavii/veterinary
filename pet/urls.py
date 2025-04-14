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
router.register(r'pet', PetViewSet, basename='pet')


urlpatterns = [

    path('cart/', CartView.as_view(), name='cart'),

    path('create-order/', create_order.as_view(), name='create_order'),
    path('update-order/<order_id>', update_order, name='update_order'),
    path('delete-order/<order_id>', delete_order, name='delete_order'),
    path('list-order-admin/', list_order_admin, name='list_order_admin'),
    path('get-order/', ListOrderView.as_view(), name='list_order'),
    
    # path("stream/token/", GenerateStreamToken.as_view()),

    path('book-daycare/', CreateDayCareBooking.as_view(), name='book_daycare'),

    path('list-day-care-bookings/', ListDayCareBookings.as_view(), name='list_daycare_bookings'),

] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
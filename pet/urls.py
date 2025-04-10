from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('list-pets/', list_pet.as_view(), name='list_pets'),
    path('register-pets/', register_pet.as_view(), name='create_pet'),
    
    path('create-pet-consultation-appointment/', create_pet_consultation_appointment.as_view(), name='create_pet_consultation_appointment'),
    path('list-pet-consultation-appointment/', list_pet_consultation_appointment.as_view(), name='list_pet_consultation_appointment'),
    
    path('create-pet-vaccination-appointment/', create_pet_vaccination_appointment.as_view(), name='create_pet_vaccination_appointment'),
    path('list-pet-vaccination-appointment/', list_pet_vaccination_appointment.as_view(), name='list_pet_vaccination_appointment'),
  
    path('create-pet-test-booking/', create_pet_test_booking.as_view(), name='create_pet_test_booking'),
    path('list-pet-test-booking/', list_pet_test_booking.as_view(), name='list_pet_test_booking'),
    
    path('cart/', CartView.as_view(), name='cart'),

    path('create-order/', create_order.as_view(), name='create_order'),
    path('update-order/<order_id>', update_order, name='update_order'),
    path('delete-order/<order_id>', delete_order, name='delete_order'),
    path('list-order-admin/', list_order_admin, name='list_order_admin'),
    path('list-order/', list_order.as_view(), name='list_order'),
  

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
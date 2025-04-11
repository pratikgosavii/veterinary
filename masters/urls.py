from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    # path('add-doctor/', add_doctor, name='add_doctor'),
    # path('add-doctor-json/', add_doctor_json, name='add_doctor_json'),
    # path('update-doctor/<doctor_id>', update_doctor, name='update_doctor'),
    path('delete-doctor/<doctor_id>', delete_doctor, name='delete_doctor'),
    path('list-doctor/', list_doctor, name='list_doctor'),

    path('add-coupon/', add_coupon, name='add_coupon'),
    path('update-coupon/<coupon_id>', update_coupon, name='update_coupon'),
    path('delete-coupon/<coupon_id>', delete_coupon, name='delete_coupon'),
    path('list-coupon/', list_coupon, name='list_coupon'),
    path('get-coupon/', get_coupon.as_view(), name='get_coupon'),

    path('add-event/', add_event, name='add_event'),
    path('update-event/<event_id>', update_event, name='update_event'),
    path('delete-event/<event_id>', delete_event, name='delete_event'),
    path('list-event/', list_event, name='list_event'),
    path('get-event/', get_event.as_view(), name='get_event'),

    path('add-testimonials/', add_testimonials, name='add_testimonials'),  # create or fetch list of admins
    path('update-testimonials/<testimonials_id>', update_testimonials, name='update_testimonials'),  # create or fetch list of admins
    path('list-testimonials/', list_testimonials, name='list_testimonials'),  # create or fetch list of admins
    path('delete-testimonials/<testimonials_id>', delete_testimonials, name='delete_testimonials'),  # create or fetch list of admins
    path('get-testimonials/', get_testimonials.as_view(), name='get_testimonials'), 

    path('add-amenity/', add_amenity, name='add_amenity'),  # create or fetch list of admins
    path('update-amenity/<amenity_id>', update_amenity, name='update_amenity'),  # create or fetch list of admins
    path('list-amenity/', list_amenity, name='list_amenity'),  # create or fetch list of admins
    path('delete-amenity/<amenity_id>', delete_amenity, name='delete_amenity'),  # create or fetch list of admins
    path('get-amenity/', get_amenity.as_view() , name='get_amenity '), 

    path('add-customer-address/', add_customer_address, name='add_customer_address'),  # create or fetch list of admins
    path('update-customer-address/<customer_address_id>', update_customer_address, name='update_customer_address'),  # create or fetch list of admins
    path('list-customer-address/', list_customer_address, name='list_customer_address'),  # create or fetch list of admins
    path('delete-customer-address/<customer_address_id>', delete_customer_address, name='delete_customer_address'),  # create or fetch list of admins
    path('get-customer-address/', get_customer_address.as_view() , name='get_customer_address '), 

    path('add-service-category/', add_service_category, name='add_service_category'),  # create or fetch list of admins
    path('update-service-category/<service_category_id>', update_service_category, name='update_service_category'),  # create or fetch list of admins
    path('list-service-category/', list_service_category, name='list_service_category'),  # create or fetch list of admins
    path('delete-service-category/<service_category_id>', delete_service_category, name='delete_service_category'),  # create or fetch list of admins
    path('get-service-category/', get_service_category.as_view(), name='get_service_category '), 

    path('add-symptom/', add_symptom, name='add_symptom'),  # create or fetch list of admins
    path('update-symptom/<symptom_id>', update_symptom, name='update_symptom'),  # create or fetch list of admins
    path('list-symptom/', list_symptom, name='list_symptom'),  # create or fetch list of admins
    path('delete-symptom/<symptom_id>', delete_symptom, name='delete_symptom'),
    path('get-symptom/', get_symptom.as_view() , name='get_symptom '), 

    path('add-service-subcategory/', add_service_subcategory, name='add_service_subcategory'),  # create or fetch list of admins
    path('update-service-subcategory/<service_subcategory_id>', update_service_subcategory, name='update_service_subcategory'),  # create or fetch list of admins
    path('list-service-subcategory/', list_service_subcategory, name='list_service_subcategory'),  # create or fetch list of admins
    path('delete-service-subcategory/<service_subcategory_id>', delete_service_subcategory, name='delete_service_subcategory'),  # create or fetch list of admins
    path('get-service-subcategory/', get_service_subcategory.as_view() , name='get_service_subcategory '), 

    path('add-service/', add_service, name='add_service'),  # create or fetch list of admins
    path('update-service/<service_id>', update_service, name='update_service'),  # create or fetch list of admins
    path('list-service/', list_service, name='list_service'),  # create or fetch list of admins
    path('delete-service/<service_id>', delete_service, name='delete_service'),  # create or fetch list of admins
    path('get-service/', get_service.as_view() , name='get_service '), 

    path('add-test/', add_test, name='add_test'),
    path('update-test/<test_id>', update_test, name='update_test'),
    path('delete-test/<test_id>', delete_test, name='delete_test'),
    path('list-test/', list_test, name='list_test'),
    path('get-test/', get_test.as_view(), name='get_test'),

    path('add-dog-breed/', add_dog_breed, name='add_dog_breed'),
    path('update-dog-breed/<dog_breed_id>', update_dog_breed, name='update_dog_breed'),
    path('delete-dog-breed/<dog_breed_id>', delete_dog_breed, name='delete_dog_breed'),
    path('list-dog-breed/', list_dog_breed, name='list_dog_breed'),
    path('get-dog-breed/', get_dog_breed.as_view(), name='get_dog_breed'),

    path('add-product/', add_product, name='add_product'),
    path('update-product/<product_id>', update_product, name='update_product'),
    path('delete-product/<product_id>', delete_product, name='delete_product'),
    path('list-product/', list_product, name='list_product'),
    path('get-product/', get_product.as_view(), name='get_product'),

    path('add-vaccination/', add_vaccination, name='add_vaccination'),
    path('update-vaccination/<vaccination_id>', update_vaccination, name='update_vaccination'),
    path('delete-vaccination/<vaccination_id>', delete_vaccination, name='delete_vaccination'),
    path('list-vaccination/', list_vaccination, name='list_vaccination'),
    path('get-vaccination/', get_vaccination.as_view(), name='get_vaccination'),


    
    path('add-home-banner/', add_home_banner, name='add_home_banner'),  # create or fetch list of admins
    path('update-home-banner/<home_banner_id>', update_home_banner, name='update_home_banner'),  # create or fetch list of admins
    path('list-home-banner/', list_home_banner, name='list_home_banner'),  # create or fetch list of admins
    path('delete-home-banner/<home_banner_id>', delete_home_banner, name='delete_home_banner'),  # create or fetch list of admins
    path('get-home-banner/', get_home_banner, name='get_home_banner'), 

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
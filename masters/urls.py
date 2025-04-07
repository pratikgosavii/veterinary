from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('add-doctor/', add_doctor, name='add_doctor'),
    path('add-doctor-json/', add_doctor_json, name='add_doctor_json'),
    path('update-doctor/<doctor_id>', update_doctor, name='update_doctor'),
    path('delete-doctor/<doctor_id>', delete_doctor, name='delete_doctor'),
    path('list-doctor/', list_doctor, name='list_doctor'),
    path('get-doctor/', get_doctor, name='get_doctor'),

    path('add-coupon/', add_coupon, name='add_coupon'),
    path('update-coupon/<coupon_id>', update_coupon, name='update_coupon'),
    path('delete-coupon/<coupon_id>', delete_coupon, name='delete_coupon'),
    path('list-coupon/', list_coupon, name='list_coupon'),
    path('get-coupon/', get_coupon, name='get_coupon'),

    path('add-testimonials/', add_testimonials, name='add_testimonials'),  # create or fetch list of admins
    path('update-testimonials/<testimonials_id>', update_testimonials, name='update_testimonials'),  # create or fetch list of admins
    path('list-testimonials/', list_testimonials, name='list_testimonials'),  # create or fetch list of admins
    path('delete-testimonials/<testimonials_id>', delete_testimonials, name='delete_testimonials'),  # create or fetch list of admins
    path('get-testimonials/', get_testimonials, name='get_testimonials'), 

    # path('add-testimonials/', add_testimonials, name='add_testimonials'),  # create or fetch list of admins
    # path('update-testimonials/<testimonials_id>', update_testimonials, name='update_testimonials'),  # create or fetch list of admins
    # path('list-testimonials/', list_testimonials, name='list_testimonials'),  # create or fetch list of admins
    # path('delete-testimonials/<testimonials_id>', delete_testimonials, name='delete_testimonials'),  # create or fetch list of admins
    path('get-amenity/', get_amenity , name='get_amenity '), 

    path('add-testimonials/', add_testimonials, name='add_testimonials'),  # create or fetch list of admins
    path('update-testimonials/<testimonials_id>', update_testimonials, name='update_testimonials'),  # create or fetch list of admins
    path('list-testimonials/', list_testimonials, name='list_testimonials'),  # create or fetch list of admins
    path('delete-testimonials/<testimonials_id>', delete_testimonials, name='delete_testimonials'),  # create or fetch list of admins
    path('get-symptom/', get_symptom , name='get_symptom '), 
    path('get-service-category/', get_service_category, name='get_service_category '), 
    path('get-service-subcategory/', get_service_subcategory , name='get_service_subcategory '), 



] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
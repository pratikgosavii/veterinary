from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [



    # path('add-day_care/', add_day_care, name='add_day_care'),
    # path('update-day_care/<int:day_care_id>/', update_day_care, name='update_day_care'),
    # path('list-day_care/', list_day_care, name='list_day_care'),
    # path('delete-day_care/<int:day_care_id>/', delete_day_care, name='delete_day_care'),
    path('get/', get_day_care.as_view(), name='get_day_care'),

    path('register/', day_care_register.as_view(), name='register_day_care'),
    path('get/<int:id>/', DayCareDetailView.as_view(), name='day-care-detail'),

    path('book-daycare/', CreateDayCareBooking.as_view(), name='book_daycare'),
    path('list-day-care-bookings/', ListDayCareBookings.as_view(), name='list_daycare_bookings'),


] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
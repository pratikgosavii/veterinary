from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import DayCareViewSet

router = DefaultRouter()
router.register('daycare', DayCareViewSet, basename='daycare')
router.register('daycare-foodmenu', DayCareFoodmenuViewSet, basename='daycarefoodmenu')


urlpatterns = [


    path('get-booking-count/', get_booking_count.as_view(), name='get_booking_count'),

    # path('add-day_care/', add_day_care, name='add_day_care'),
    # path('update-day_care/<int:day_care_id>/', update_day_care, name='update_day_care'),
    # path('list-day_care/', list_day_care, name='list_day_care'),
    # path('delete-day_care/<int:day_care_id>/', delete_day_care, name='delete_day_care'),
    path('get/', get_day_care.as_view(), name='get_day_care'),

    # path('register/', day_care_register.as_view(), name='register_day_care'),
    path('get/<int:id>/', DayCareDetailView.as_view(), name='day-care-detail'),

    path('food-menu/<int:daycare_id>/', DayCareFoodMenuListView.as_view(), name='daycare-food-menus'),

    path('list-day-care-bookings/', ListDayCareBookings.as_view(), name='list_daycare_bookings'),


] + router.urls  

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
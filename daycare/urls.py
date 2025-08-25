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
    
    path('get/', get_day_care.as_view(), name='get_day_care'),
    path('get/<int:id>/', DayCareDetailView.as_view(), name='day-care-detail'),

    path('food-menu/<int:daycare_id>/', DayCareFoodMenuListView.as_view(), name='daycare-food-menus'),

    path('list-day-care-bookings/', ListDayCareBookings.as_view(), name='list_daycare_bookings'),


] + router.urls  

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
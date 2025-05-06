"""
URL configuration for vetinary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

from .views import *



from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vendor-kyc', VendorKYCViewSet, basename='vendor-kyc')
router.register(r'service-history', serviceHistoryViewSet, basename='serviceHistoryViewSet')

urlpatterns = [
   
    path('all-open-bookings/', all_open_bookings.as_view({'get': 'list'}), name='all_open_bookings'),
    path('all-vendor-bookings/', all_vendor_bookings.as_view({'get': 'list'}), name='all_vendor_bookings'),

    path('accept-order/', accept_order.as_view(), name='accept_order'),

    # path('all-open-bookings-doctor/', all_open_bookings_doctor.as_view({'get': 'list'}), name='all_open_bookings_doctor'),
    # path('all-open-bookings-doctor-daycare/', all_open_bookings_daycare.as_view(), name='all_open_bookings_daycare'),
    # path('all-open-bookings-service-provider/', all_open_bookings_service_provider.as_view(), name='all_open_bookings_service_provider'),
    
    path('all-bookings-count/', all_bookings_count.as_view({'get': 'list'}), name='all_bookings_count'),

    path('kyc-list/', kyc_list, name='kyc_list'),
   
    path('admin-all-booking/', admin_all_booking, name='admin_all_booking'),
    path('admin-all-open-booking/', admin_all_open_booking, name='admin_all_open_booking'),






] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
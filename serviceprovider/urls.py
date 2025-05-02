from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'service-provider', ServiceProviderViewSet, basename='service-provider')

urlpatterns = [

    
    path('get-services-count/', get_services_count.as_view(), name='get_services_count'),

    path('list-serviceprovider-bookings/', ListServiceproviderBookings.as_view(), name='list_serviceprovider_bookings'),

    # path('add-service_provider/', add_service_provider, name='add_service_provider'),
    # path('update-service_provider/<int:service_provider_id>/', update_service_provider, name='update_service_provider'),
    # path('list-service_provider/', list_service_provider, name='list_service_provider'),
    # path('delete-service_provider/<int:service_provider_id>/', delete_service_provider, name='delete_service_provider'),
    # path('get-service_provider/', get_service_provider, name='get_service_provider'),

    # path('login-service_provider/', service_provider_login.as_view(), name='login_service_provider'),
    # path('signup-service_provider/', service_provider_signup.as_view(), name='signup_service_provider'),

    path('get-service-providers/', get_service_providers.as_view(), name='get_service_providers'),


] + router.urls  

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
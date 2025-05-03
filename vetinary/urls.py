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

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('admin/', admin.site.urls),
    path('masters/', include('masters.urls')),
    path('daycare/', include('daycare.urls')),
    path('doctor/', include('doctor.urls')),
    path('pet/', include('pet.urls')),
    path('masters/', include('masters.urls')),
    path('serviceprovider/', include('serviceprovider.urls')),
    path('users/', include('users.urls')),
    path('vendor/', include('vendor.urls')),


]

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version='v1',
      description="Your API description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="you@example.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    # your other paths...
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
import django_filters
from .models import *

class service_providersFilter(django_filters.FilterSet):
   
    
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = service_provider
        fields = ['status']

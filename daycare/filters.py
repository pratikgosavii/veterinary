import django_filters
from daycare.models import day_care_booking

class DayCareBookingFilter(django_filters.FilterSet):
    
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = day_care_booking
        fields = ['status']

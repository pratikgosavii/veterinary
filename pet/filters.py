import django_filters
from .models import order
from users.models import *

class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    # Add more filters as needed

    class Meta:
        model = order
        fields = ['status', 'user']  # You can add more fields as per your requirement

import django_filters
from .models import *

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = event
        exclude = ['image']  # ⛔ Exclude unsupported field

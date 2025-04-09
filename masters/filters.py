import django_filters
from .models import *

class serviceFilter(django_filters.FilterSet):
    class Meta:
        model = service
        exclude = ['image']  # ⛔ Exclude unsupported field

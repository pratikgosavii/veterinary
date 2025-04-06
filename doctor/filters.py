import django_filters
from .models import *

class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = doctor
        exclude = ['image']  # ⛔ Exclude unsupported field

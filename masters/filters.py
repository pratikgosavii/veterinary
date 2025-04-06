# import django_filters
# from django_filters import DateFilter, CharFilter, DateTimeFilter
# from django.forms.widgets import DateInput
# from django import forms

# from .models import *
# from .forms import *

# from django_filters import FilterSet, ChoiceFilter, NumberFilter
# from users.models import *

# class transactions_filter(django_filters.FilterSet):

#     investor = django_filters.ModelChoiceFilter(
#         queryset=investor.objects.all(),
#         field_name='investor',
#         widget=forms.Select(attrs={'class': 'form-control cus_dro', 'id': 'investor'}),
#     )

#     operator = django_filters.ModelChoiceFilter(
#         queryset=operator.objects.all(),
#         field_name='operator',
#         widget=forms.Select(attrs={'class': 'form-control cus_dro', 'id': 'operator'}),
#     )

#     timestamp_from = django_filters.DateTimeFilter(
#         field_name='timestamp',
#         lookup_expr='gte',  # Greater than or equal to (from date)
#         label='Timestamp From',
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control',
#             'type': 'datetime-local'  # Allows users to select both date and time
#         }),
#     )

#     timestamp_to = django_filters.DateTimeFilter(
#         field_name='timestamp',
#         lookup_expr='lte',  # Less than or equal to (to date)
#         label='Timestamp To',
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control',
#             'type': 'datetime-local'
#         }),
#     )

#     class Meta:
#         model = transactions
#         fields = ['investor', 'operator', 'timestamp_from', 'timestamp_to']

    


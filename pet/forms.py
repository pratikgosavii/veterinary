from django import forms
from .models import order, pet


class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['total'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        items_data = self.data.get('items')  # Get it from POST data
        # You can validate it or store it temporarily
        print("Items JSON from frontend:", items_data)
        return cleaned_data
    



from django import forms
from .models import (
    consultation_appointment,
    online_consultation_appointment,
    vaccination_appointment,
    test_booking,
    service_booking,
    day_care_booking,
)

class BaseBootstrapForm(forms.ModelForm):
    """Base form to add Bootstrap form-control class to all fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add 'form-control' class for all except checkbox or  select
            if isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelect, forms.RadioSelect)):
                # For checkboxes, add 'form-check-input'
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (existing_classes + ' form-check-input').strip()
            elif isinstance(field.widget, forms.Select):
                # For multi-selects, add 'form-select' + set size for better UI
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (existing_classes + ' form-control').strip()
                field.widget.attrs['size'] = '5'
            else:
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

from django import forms
from .models import (
    consultation_appointment,
    online_consultation_appointment,
    vaccination_appointment,
    test_booking,
    service_booking,
    day_care_booking
)


class ConsultationAppointmentForm(forms.ModelForm):
    class Meta:
        model = consultation_appointment
        fields = ['pet', 'consultation_type', 'symptom', 'doctor', 'date', 'status', 'amount']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'consultation_type': forms.Select(attrs={'class': 'form-control'}),
            'symptom': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = pet.objects.filter(owner=user)  # Adjust model if needed


class OnlineConsultationAppointmentForm(forms.ModelForm):
    class Meta:
        model = online_consultation_appointment
        fields = ['pet', 'online_consultation_type', 'symptom', 'doctor', 'date', 'status', 'amount']
        widgets = {
           'pet': forms.Select(attrs={'class': 'select2'}),
            'online_consultation_type': forms.Select(attrs={'class': 'select2'}),
            'symptom': forms.Select(attrs={'class': 'select2'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = pet.objects.filter(owner=user)  # Adjust model if needed


class VaccinationAppointmentForm(forms.ModelForm):
    class Meta:
        model = vaccination_appointment
        fields = ['pet', 'vaccination', 'doctor', 'date', 'address', 'status', 'amount']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'vaccination': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = pet.objects.filter(owner=user)  # Adjust model if needed


class TestBookingForm(forms.ModelForm):
    class Meta:
        model = test_booking
        fields = ['pet', 'test', 'doctor', 'date', 'address', 'status', 'amount']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'test': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = pet.objects.filter(owner=user)  # Adjust model if needed


class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = service_booking
        fields = ['service_provider', 'pets', 'services', 'date', 'address', 'at_home', 'status', 'amount']
        widgets = {
            'service_provider': forms.Select(attrs={'class': 'form-control'}),
            'pets': forms.Select(attrs={'class': 'form-control'}),
            'services': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'at_home': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = pet.objects.filter(owner=user)  # Adjust model if needed


class DayCareBookingForm(forms.ModelForm):
    class Meta:
        model = day_care_booking
        fields = ['daycare', 'pets', 'food_selection', 'date_from', 'date_to', 'half_day', 'full_day', 'status', 'total_cost']
        widgets = {
            'daycare': forms.Select(attrs={'class': 'form-control'}),
            'pets': forms.Select(attrs={'class': 'form-control'}),
            'food_selection': forms.SelectMultiple(attrs={'class': 'select'}),
            'date_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'half_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'full_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pets'].queryset = pet.objects.filter(owner=user)  # Adjust model if needed

from django import forms
from .models import order

class order_Form(forms.ModelForm):
    class Meta:
        model = order
        fields = ['user', 'products', 'total', 'status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'products': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

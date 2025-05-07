from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


from django import forms
from .models import vendor_kyc

class vendor_kyc_Form(forms.ModelForm):
    class Meta:
        model = vendor_kyc
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control', 'id': 'user'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control', 'id': 'image'
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-control', 'id': 'document_type'
            }),
            'document_image': forms.ClearableFileInput(attrs={
                'class': 'form-control', 'id': 'document_image'
            }),
            'approved': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 'id': 'approved'
            }),
        }

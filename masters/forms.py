from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class coupon_Form(forms.ModelForm):
    class Meta:
        model = coupon
        fields = '__all__'  # Include all fields
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'min_purchase': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }




class testimonials_Form(forms.ModelForm):
    class Meta:
        model = testimonials
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
          
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'price'
            }),

        }


        
class test_Form(forms.ModelForm):
    class Meta:
        model = test
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'mrp': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mrp'
            }),

            
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'description'
            }),
            
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active'}),
            
        }




        
class dog_breed_Form(forms.ModelForm):
    class Meta:
        model = dog_breed
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            })

        }

        
class amenity_Form(forms.ModelForm):
    class Meta:
        model = amenity
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            })

        }

        
class service_category_Form(forms.ModelForm):
    class Meta:
        model = service_category
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),


        }
        
class symptom_Form(forms.ModelForm):
    class Meta:
        model = symptom
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),



        }
        
class service_subcategory_Form(forms.ModelForm):
    class Meta:
        model = service_subcategory
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control', 'id': 'category'
            }),

            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),


        }
        
class service_Form(forms.ModelForm):
    class Meta:
        model = service
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control', 'id': 'category'
            }),

            'subcategory': forms.Select(attrs={
                'class': 'form-control', 'id': 'subcategory'
            }),

            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),

            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),


        }




class product_category_Form(forms.ModelForm):
    class Meta:
        model = product_category
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),


        }

class product_Form(forms.ModelForm):
    class Meta:
        model = product
        fields = ['name', 'category', 'description', 'image', 'price', 'rating', 'is_popular', 'is_featured', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }




class vaccination_Form(forms.ModelForm):
    class Meta:
        model = vaccination
        fields = ['name', 'disease', 'description', 'age_limit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'disease': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control description-box'}),
            'age_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class event_Form(forms.ModelForm):
    class Meta:
        model = event
        fields = ['name', 'image', 'description', 'start_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control description-box'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),

        }




class customer_address_Form(forms.ModelForm):
    class Meta:
        model = customer_address
        fields = ['name', 'type', 'address', 'landmark', 'pin_code', 'city', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }
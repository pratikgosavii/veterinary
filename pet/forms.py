from django import forms
from .models import order


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
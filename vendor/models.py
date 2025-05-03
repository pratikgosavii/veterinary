from django.db import models

# Create your models here.


from django.db import models

# Create your models here.

from users.models import *
from masters.models import *
from pet.models import *



DOCUMENT_CHOICES = [
    ('adhar_card', 'Adhar Card'),
    ('driving_licence', 'Driving Licence'),
    ('passport', 'Passport'),
]


class vendor_kyc(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vendor_kyc/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, default='open')
    document_image = models.ImageField(upload_to='vendor_kyc/')
    approved = models.BooleanField(default=False)

    
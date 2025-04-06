from django.db import models

# Create your models here.

from users.models import *
from masters.models import *
from pet.models import *



class service_provider(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    service_center_name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class service_booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ManyToManyField('masters.service')
    pets = models.ManyToManyField('pet.pet')
    date = models.DateTimeField()
    address = models.TextField(null=True, blank=True)
    at_home = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)

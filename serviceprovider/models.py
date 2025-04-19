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
    
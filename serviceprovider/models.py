from django.db import models

# Create your models here.

from users.models import *
from masters.models import *
from pet.models import *



class service_provider(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor_images/')
    service_center_name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
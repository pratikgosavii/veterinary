from django.db import models

# Create your models here.


from users.models import *
from masters.models import *
from pet.models import *





class day_care(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    images = models.ImageField(upload_to='daycare_photos/', null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price_half_day = models.FloatField(null=True, blank=True)
    price_full_day = models.FloatField(null=True, blank=True)
    amenities = models.ManyToManyField('masters.amenity', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

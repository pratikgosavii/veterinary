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
    price_per_hour = models.FloatField(null=True, blank=True)
    price_per_day = models.FloatField(null=True, blank=True)
    amenities = models.ManyToManyField('masters.amenity', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)


class day_care_booking(models.Model):
    daycare = models.ForeignKey(day_care, on_delete=models.CASCADE)
    pets = models.ManyToManyField('pet.pet')
    date_from = models.DateField()
    date_to = models.DateField()
    drop_off = models.BooleanField()
    pick_up = models.BooleanField()
    food_selection = models.TextField()
    payment_status = models.BooleanField(default=False)
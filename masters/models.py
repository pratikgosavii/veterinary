from django.db import models


from users.models import User
from django.utils.timezone import now
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')



from users.models import User




class amenity(models.Model):
    name = models.CharField(max_length=255)



class coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Unique coupon code
    title = models.CharField(max_length=50)  # Unique coupon code
    description = models.CharField(max_length=500, null=True, blank=True)  # Field for time slots
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 10%
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Max ₹1000 discount
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Min cart value required
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Cap on discount
    image = models.ImageField(upload_to='doctor_images/')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    


from django.db import models
from django.contrib.auth.models import AbstractUser


class service_category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class service_subcategory(models.Model):
    category = models.ForeignKey(service_category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

class service(models.Model):
    category = models.ForeignKey(service_category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(service_subcategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()


class symptom(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='symptom_images/', null=True, blank=True)





class address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    address = models.TextField()
    landmark = models.CharField(max_length=255, null=True, blank=True)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)




# services

# doctor & symptom models
# day care (boarding)
# boarding booking
# from pet.models import *

# address
# consultation booking
# # product management
# class product_category(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='category_images/', null=True, blank=True)

# class product(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(product_category, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images/', null=True, blank=True)
#     rating = models.FloatField(default=0)
#     review = models.TextField(null=True, blank=True)
#     price = models.FloatField()

# class product_order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     delivery_address = models.ForeignKey(address, on_delete=models.CASCADE)
#     payment_status = models.BooleanField(default=False)

# video call history



class testimonials(models.Model):
    
    name = models.CharField(max_length=100)  # Field for time slots
    description = models.CharField(max_length=500)  # Field for time slots
    rating = models.DecimalField(max_digits=3, decimal_places=1, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    

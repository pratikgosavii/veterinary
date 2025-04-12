from django.db import models

# Create your models here.



from users.models import *
from masters.models import *



# pet profile
class pet(models.Model):
    dog = 'dog'
    cat = 'cat'
    pet_type_choices = [(dog, 'dog'), (cat, 'cat')]

    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='pet_photos/', null=True, blank=True)
    pet_type = models.CharField(max_length=10, choices=pet_type_choices)
    breed = models.ForeignKey(dog_breed, on_delete=models.CASCADE)
    born_date = models.DateField()
    age = models.IntegerField()
    productive_status = models.CharField(max_length=255)
    weight = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

# medical details
class medical_report(models.Model):
    pet = models.ManyToManyField('pet.pet')
    title = models.CharField(max_length=255)
    report = models.TextField()
    date = models.DateField()

# appointment & orders
class consultation_appointment(models.Model):
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField('pet.pet')
    symptom = models.ManyToManyField('masters.symptom')
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)

# appointment & orders
class vaccination_appointment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField('pet.pet')
    vaccination = models.ManyToManyField('masters.vaccination')
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)

# appointment & orders
class test_booking(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField('pet.pet')
    test = models.ManyToManyField('masters.test')
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)
    report = models.FileField(upload_to='reports/', null=True, blank=True)

# vaccination
class pet_vaccination(models.Model):
    pet = models.ManyToManyField('pet.pet')
    age = models.IntegerField()
    additional_questions = models.JSONField()
    date_given = models.DateField()

# lab reports
class lab_report(models.Model):
    pet = models.ManyToManyField('pet.pet')
    report = models.TextField()
    date = models.DateField()

# food preference
class food_preference(models.Model):
    pet = models.ManyToManyField('pet.pet')
    preference = models.TextField()

    

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Generic relation to any service item (product, service, test, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')




class order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('packing', 'Packing'),
        ('delay', 'Taking Time More Than Usual'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(product)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
from django.db import models

# Create your models here.



from daycare.models import *
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
    consultation_type = models.ManyToManyField('masters.consultation_type')
    symptom = models.ManyToManyField('masters.symptom')
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)

# appointment & orders
class online_consultation_appointment(models.Model):
     
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField('pet.pet')
    online_consultation_type = models.ManyToManyField('masters.online_consultation_type')
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
    

class ConsultationAppointmentReport(models.Model):
    appointment = models.ForeignKey(consultation_appointment, on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/consultation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class OnlineConsultationAppointmentReport(models.Model):
    appointment = models.ForeignKey(online_consultation_appointment, on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/online_consultation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class TestBookingReport(models.Model):
    booking = models.ForeignKey(test_booking, on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/test_booking/')
    uploaded_at = models.DateTimeField(auto_now_add=True)




class day_care_booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    daycare = models.ForeignKey("daycare.day_care", on_delete=models.CASCADE)
    pets = models.ManyToManyField('pet.pet')
    food_selection = models.ManyToManyField('masters.food_menu')  # ✅ Keep only this one

    date_from = models.DateField()
    date_to = models.DateField()
    
    payment_status = models.BooleanField(default=False)

    half_day = models.BooleanField(default=False)
    full_day = models.BooleanField(default=False)

    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    
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
    
    product = models.ForeignKey(product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')


class order_item(models.Model):
    order = models.ForeignKey(order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

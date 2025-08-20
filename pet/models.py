from django.db import models

# Create your models here.



from daycare.models import *
from pet.utils import get_next_booking_id
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

    def __str__(self):
        return self.name  # instead of <pet: name>
    
    
# medical details
class medical_report(models.Model):
    pet = models.ManyToManyField('pet.pet')
    title = models.CharField(max_length=255)
    report = models.TextField()
    date = models.DateField()



STATUS_CHOICES = [
    ('open', 'Open'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class BookingSequence(models.Model):
    last_id = models.IntegerField(default=0)


# appointment & orders
class consultation_appointment(models.Model):
    
    booking_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField("pet.pet")
    consultation_type = models.ForeignKey('masters.consultation_type', on_delete=models.CASCADE)
    symptom = models.ManyToManyField('masters.symptom')
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = get_next_booking_id()
        super().save(*args, **kwargs)


# appointment & orders
class online_consultation_appointment(models.Model):
    
    booking_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField("pet.pet")
    online_consultation_type = models.ForeignKey('masters.online_consultation_type', on_delete=models.CASCADE)
    symptom = models.ManyToManyField('masters.symptom')
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = get_next_booking_id()
        super().save(*args, **kwargs)


# appointment & orders
class vaccination_appointment(models.Model):
    
    booking_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField("pet.pet")
    vaccination = models.ForeignKey('masters.vaccination', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    address = models.ForeignKey('masters.customer_address', on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = get_next_booking_id()
        super().save(*args, **kwargs)


# appointment & orders
class test_booking(models.Model):
    
    booking_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ManyToManyField("pet.pet")
    test = models.ForeignKey('masters.test', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.doctor', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    address = models.ForeignKey('masters.customer_address', on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = get_next_booking_id()
        super().save(*args, **kwargs)

from serviceprovider.models import *

class service_booking(models.Model):
    
    booking_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    service_provider = models.ForeignKey("serviceprovider.service_provider", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ForeignKey('masters.service', null=True, blank=True, on_delete=models.CASCADE)
    pets = models.ManyToManyField("pet.pet")
    date = models.DateTimeField()
    address = models.ForeignKey('masters.customer_address', on_delete=models.CASCADE)
    at_home = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = get_next_booking_id()
        super().save(*args, **kwargs)




class day_care_booking(models.Model):

    booking_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    daycare = models.ForeignKey("daycare.day_care", on_delete=models.CASCADE, null=True, blank=True)
    pets = models.ManyToManyField("pet.pet")
    food_selection = models.ManyToManyField('masters.food_menu')  # ✅ Keep only this one

    date_from = models.DateField()
    date_to = models.DateField()
    
    payment_status = models.BooleanField(default=False)

    half_day = models.BooleanField(default=False)
    full_day = models.BooleanField(default=False)

    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')


    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = get_next_booking_id()
        super().save(*args, **kwargs)
    



from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class SupportTicket(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    # Generic relation to any appointment model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    appointment = GenericForeignKey('content_type', 'object_id')

    subject = models.CharField(max_length=255)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.pk} - {self.subject}"
    

    @property
    def booking_url(self):
        """
        Return the correct update URL for the related booking
        """
        model = self.content_type.model

        mapping = {
            "consultation_appointment": "consultation_update",
            "online_consultation_appointment": "online_consultation_update",
            "vaccination_appointment": "vaccination_update",
            "test_booking": "test_update",
            "day_care_booking": "daycare_update",
            "service_booking": "service_update",
        }

        url_name = mapping.get(model)
        if url_name:
            return reverse(url_name, args=[self.object_id])
        return "#"

class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# vaccination
class pet_vaccination(models.Model):
    pet = models.ManyToManyField('pet.pet')
    age = models.IntegerField()
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
    address = models.ForeignKey('masters.customer_address', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')


class order_item(models.Model):
    order = models.ForeignKey(order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)




class PastVaccination(models.Model):
    user = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='reports')
    pet = models.ForeignKey('pet.pet', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    report = models.FileField(upload_to='reports/test_booking/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    



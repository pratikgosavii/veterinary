from django.db import models

# Create your models here.


from masters.models import *
from users.models import User
from pet.models import *



class doctor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False)
    image = models.ImageField(upload_to='doctor_images/')
    address = models.CharField(max_length=120, unique=False)
    mobile_no = models.IntegerField(null = True, blank = True)
    experience = models.IntegerField(null = True, blank = True)
    title = models.CharField(max_length=120, unique=False)
    degree = models.CharField(max_length=120, unique=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null = True, blank = True)
    remark = models.CharField(max_length=120, unique=False, null = True, blank = True)
    is_active = models.BooleanField(default = True)

    
    def __str__(self):
        return self.name
    
    

class consultation_booking(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    symptom = models.ManyToManyField('masters.symptom')
    pets = models.ManyToManyField('pet.pet')
    date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)



class video_call_history(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

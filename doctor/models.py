from django.db import models

# Create your models here.


from masters.models import *
from users.models import User
from pet.models import *

from datetime import datetime

def current_time():
    return datetime.now().time()

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
        
    available_from = models.TimeField(default=current_time)  # ✅ GOOD
    available_to = models.TimeField(default=current_time)  

    
    def __str__(self):
        return self.name
    
    


class video_call_history(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



STATUS_CHOICES = [
    ('open', 'Open'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class ConsultationAppointmentReport(models.Model):
    appointment = models.ForeignKey(consultation_appointment, on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/consultation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

class OnlineConsultationAppointmentReport(models.Model):
    appointment = models.ForeignKey(online_consultation_appointment, on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/online_consultation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

class TestBookingReport(models.Model):
    booking = models.ForeignKey(test_booking, on_delete=models.CASCADE, related_name='reports')
    report = models.FileField(upload_to='reports/test_booking/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

from django.db import models

# Create your models here.


from masters.models import *
from users.models import User
from pet.models import *

from datetime import datetime

def current_time():
    return datetime.now().time()

class doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    appointment = models.ForeignKey("pet.consultation_appointment", on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/consultation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

class OnlineConsultationAppointmentReport(models.Model):
    appointment = models.ForeignKey("pet.online_consultation_appointment", on_delete=models.CASCADE, related_name='reports')
    file = models.FileField(upload_to='reports/online_consultation/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

class TestBookingReport(models.Model):
    booking = models.ForeignKey(test_booking, on_delete=models.CASCADE, related_name='reports')
    report = models.FileField(upload_to='reports/test_booking/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

class VaccinationBookingReport(models.Model):
    booking = models.ForeignKey(vaccination_appointment, on_delete=models.CASCADE, related_name='reports')
    report = models.FileField(upload_to='reports/test_booking/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


class Apoinments_video_details(models.Model):
    appoinment_id = models.CharField(max_length=150)
    call_id = models.CharField(max_length=150)
    token = models.CharField(max_length=150)
    doctor = models.CharField(max_length=150)


class Prescription(models.Model):
    consultation = models.ForeignKey('pet.consultation_appointment', on_delete=models.CASCADE, related_name='fghprescriptions')
    medicine_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} - ₹{self.price}"

from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(doctor)
admin.site.register(TestBookingReport)
admin.site.register(OnlineConsultationAppointmentReport)
admin.site.register(ConsultationAppointmentReport)

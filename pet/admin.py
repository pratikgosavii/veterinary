from django.contrib import admin

# Register your models here.


from .models import  *

admin.site.register(pet)
admin.site.register(order)
admin.site.register(vaccination_appointment)
admin.site.register(test_booking)
admin.site.register(pet_vaccination)
admin.site.register(consultation_appointment)
admin.site.register(cart)
admin.site.register(service_booking)
admin.site.register(order_item)
admin.site.register(day_care_booking)
admin.site.register(online_consultation_appointment)
admin.site.register(BookingSequence)
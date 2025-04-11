from django.contrib import admin

# Register your models here.


from .models import  *

admin.site.register(pet)
admin.site.register(order)
admin.site.register(vaccination_appointment)
admin.site.register(test_booking)
admin.site.register(pet_vaccination)
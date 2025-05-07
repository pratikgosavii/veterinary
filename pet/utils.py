# bookings/utils.py
from django.db import transaction

def get_next_booking_id():

    from pet.models import BookingSequence
    with transaction.atomic():
        obj, _ = BookingSequence.objects.select_for_update().get_or_create(pk=1)
        obj.last_id += 1
        obj.save()
        return obj.last_id

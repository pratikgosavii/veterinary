from rest_framework import serializers

from doctor.serializer import doctor_serializer

from .models import *



from rest_framework import serializers
from .models import *


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = pet
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['owner'] = request.user
        return super().create(validated_data)
    


from masters.serializers import *



from masters.serializers import *

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType



class CartSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all(), write_only=True)
    product_data = product_category_serializer(source='product', read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = cart
        fields = ['product', 'product_data', 'quantity']
    
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)



from doctor.models import *

    
class consultation_appointment_Serializer(serializers.ModelSerializer):


# Write-only fields for POST
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True, source="pet"
    )
    symptom_ids = serializers.PrimaryKeyRelatedField(
        queryset=symptom.objects.all(), many=True, write_only=True, source="symptom"
    )
    consultation_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=consultation_type.objects.all(), many=True, write_only=True, source="consultation_type"
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(), write_only=True, source="doctor"
    )


    pet = PetSerializer(many=True, read_only=True)
    symptom = symptom_serializer(many=True, read_only=True)
    consultation_type = consultation_type_serializer(many=True, read_only=True)
    doctor = doctor_serializer(read_only=True)

    

    class Meta:
        model = consultation_appointment
        fields = [
            'id', 'pet', 'pet_ids',
            'symptom', 'symptom_ids',
            'consultation_type', 'consultation_type_ids',
            'doctor', 'doctor_id',
            'date', 'payment_status'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    


from masters.serializers import *
    
class online_consultation_appointment_Serializer(serializers.ModelSerializer):


    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True, source="pet"
    )
    symptom_ids = serializers.PrimaryKeyRelatedField(
        queryset=symptom.objects.all(), many=True, write_only=True, source="symptom"
    )
    online_consultation_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=online_consultation_type.objects.all(), many=True, write_only=True, source="online_consultation_type"
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(), write_only=True, source="doctor"
    )

    pet = PetSerializer(many=True, read_only=True)
    symptom = symptom_serializer(many=True, read_only=True)
    doctor = doctor_serializer(read_only=True)
    online_consultation_type = online_consultation_type_serializer(many=True, read_only=True)

    class Meta:
        model = online_consultation_appointment
        fields = [
            'id', 'pet', 'pet_ids',
            'symptom', 'symptom_ids',
            'online_consultation_type_ids',
            'doctor', 'doctor_id',
            'date', 'payment_status', 'online_consultation_type'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    



from masters.serializers import *

class vaccination_appointment_Serializer(serializers.ModelSerializer):
    

    # Write-only fields for POST
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True, source="pet"
    )
    vaccination_ids = serializers.PrimaryKeyRelatedField(
        queryset=vaccination.objects.all(), many=True, write_only=True, source="vaccination"
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(), write_only=True, source="doctor"
    )

    # Read-only nested serializers
    pet = PetSerializer(many=True, read_only=True)
    vaccination = vaccination_serializer(many=True, read_only=True)
    doctor = doctor_serializer(read_only=True)

    class Meta:
        model = vaccination_appointment
        fields = [
            'id', 'pet', 'pet_ids',
            'vaccination', 'vaccination_ids',
            'doctor', 'doctor_id',
            'date', 'payment_status'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    



class test_booking_Serializer(serializers.ModelSerializer):

    test_ids = serializers.PrimaryKeyRelatedField(
        queryset=test.objects.all(), many=True, write_only=True, source='test'
    )
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True, source='pet'
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(), write_only=True, source='doctor'
    )

    test = test_serializer(many=True, read_only=True)
    pet = PetSerializer(many=True, read_only=True)
    doctor = doctor_serializer(read_only=True)

    class Meta:
        model = test_booking
        fields = ['id', 'pet', 'pet_ids', 'test', 'test_ids', 'doctor', 'doctor_id', 'date', 'payment_status']
        read_only_fields = ['user']
       

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)


    

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import order, order_item


from daycare.serializers import *

class DayCareBookingSerializer(serializers.ModelSerializer):
    
    daycare = day_care_serializer(read_only=True)
    pets = PetSerializer(many=True, read_only=True)
    food_selection = food_menu_serializer(many=True, read_only=True)

    # For writing
    daycare_id = serializers.PrimaryKeyRelatedField(
        queryset=day_care.objects.all(), write_only=True, source='daycare'
    )
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True
    )
    food_selection_ids = serializers.PrimaryKeyRelatedField(
        queryset=food_menu.objects.all(), many=True, write_only=True, source='food_selection'
    )

    class Meta:
        model = day_care_booking
        fields = [
            'id', 'user', 'daycare', 'daycare_id',
            'pets', 'pet_ids',
            'food_selection', 'food_selection_ids',
            'date_from', 'date_to',
            'half_day', 'full_day',
            'payment_status', 'total_cost'
        ]
        read_only_fields = ['id', 'user', 'daycare', 'pets', 'food_selection', 'total_cost', 'payment_status']

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        half_in = data.get('half_day', False)
        half_out = data.get('full_day', False)

        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("date_from must be before or equal to date_to")

        if date_from == date_to and half_in and half_out:
            raise serializers.ValidationError("Can't select both half-day check-in and check-out on same day.")

        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        pets = validated_data.pop('pet_ids', [])
        food_items = validated_data.pop('food_selection', [])
        daycare = validated_data.pop('daycare')

        validated_data['user'] = user

        booking = day_care_booking.objects.create(daycare=daycare, **validated_data)
        booking.pets.set(pets)
        booking.food_selection.set(food_items)
        booking.save()

        return booking

    


class OrderItemSerializer(serializers.ModelSerializer):
    
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all())
    product_details = product_category_serializer(source='product', read_only=True)

    class Meta:
        model = order_item
        fields = ['product', 'quantity', 'product_details']



class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True)

    class Meta:
        model = order
        fields = ['id', 'user', 'total', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order_instance = order.objects.create(user=self.context['request'].user, **validated_data)

        for item_data in items_data:
            order_item.objects.create(order=order_instance, **item_data)

        return order_instance
    

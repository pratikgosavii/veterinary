from rest_framework import serializers

from doctor.serializer import doctor_serializer

from .models import *



from rest_framework import serializers
from .models import *


class PetSerializer(serializers.ModelSerializer):

    vaccinations = serializers.SerializerMethodField()

    def get_vaccinations(self, obj):
        vaccinations = pet_vaccination.objects.filter(pet=obj)
        return PastVaccinationSerializer(vaccinations, many=True).data

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
    product_data = product_serializer(source='product', read_only=True)
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
    # Single pet (ForeignKey)
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(),
        many=True,
        write_only=True,
        source='pet'
    )

    symptom_ids = serializers.PrimaryKeyRelatedField(
        queryset=symptom.objects.all(),
        many=True,
        write_only=True,
        source='symptom'
    )

    consultation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=consultation_type.objects.all(),
        write_only=True,
        source='consultation_type'
    )

    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(),
        write_only=True,
        source='doctor',
        required=False,
        allow_null=True
    )

    # Read-only nested fields
    pet = PetSerializer(many=True, read_only=True)
    symptom = symptom_serializer(many=True, read_only=True)
    consultation_type = consultation_type_serializer(read_only=True)
    doctor = doctor_serializer(read_only=True)

    class Meta:
        model = consultation_appointment
        fields = [
            'id', 'pet', 'pet_id',
            'symptom', 'symptom_ids',
            'consultation_type', 'consultation_type_id',
            'doctor', 'doctor_id',
            'date', 'payment_status', 'status', 'amount', 'booking_id'
        ]
        read_only_fields = ['user', 'booking_id']

    def create(self, validated_data):
        request = self.context['request']
        symptoms = validated_data.pop('symptom')
        pets = validated_data.pop('pet')
        validated_data['user'] = request.user

        instance = consultation_appointment.objects.create(**validated_data)
        instance.symptom.set(symptoms)
        instance.pet.set(pets)
        return instance




from masters.serializers import *
    

class online_consultation_appointment_Serializer(serializers.ModelSerializer):
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(),
        many=True,
        write_only=True,
        source="pet"
    )
    symptom_ids = serializers.PrimaryKeyRelatedField(
        queryset=symptom.objects.all(),
        many=True,
        write_only=True,
        source='symptom'
    )
    online_consultation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=online_consultation_type.objects.all(),
        write_only=True,
        source="online_consultation_type"
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(),
        write_only=True,
        source="doctor",
        required=False,
        allow_null=True
    )

    pet = PetSerializer(many=True, read_only=True)
    symptom = symptom_serializer(many=True, read_only=True)
    doctor = doctor_serializer(read_only=True)
    online_consultation_type = online_consultation_type_serializer(read_only=True)

    class Meta:
        model = online_consultation_appointment
        fields = [
            'id', 'pet', 'pet_ids',
            'symptom', 'symptom_ids',
            'doctor', 'doctor_id',
            'date', 'payment_status',
            'online_consultation_type', 'online_consultation_type_id',
            'amount'
        ]
        read_only_fields = ['user', 'booking_id']

    
    def create(self, validated_data):
        request = self.context['request']
        symptoms = validated_data.pop('symptom')
        validated_data['user'] = request.user
        instance = online_consultation_appointment.objects.create(**validated_data)
        instance.symptom.set(symptoms)
        return instance


from masters.serializers import *
from masters.models import *

class vaccination_appointment_Serializer(serializers.ModelSerializer):
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True, source="pet"
    )
    vaccination_id = serializers.PrimaryKeyRelatedField(
        queryset=vaccination.objects.all(), write_only=True, source="vaccination"
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=doctor.objects.all(), write_only=True, source="doctor", required=False, allow_null=True
    )
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=customer_address.objects.all(), write_only=True, source="address"
    )

    pet = PetSerializer(many=True, read_only=True)
    vaccination = vaccination_serializer(read_only=True)
    doctor = doctor_serializer(read_only=True)
    address = customer_address_serializer(read_only=True)

    class Meta:
        model = vaccination_appointment
        fields = [
            'id', 'pet', 'pet_ids',
            'vaccination', 'vaccination_id',
            'doctor', 'doctor_id',
            'address', 'address_id',
            'date', 'payment_status', 'amount'
        ]
        read_only_fields = ['user', 'booking_id']

    def create(self, validated_data):
        request = self.context['request']
        pets = validated_data.pop('pet')
        validated_data['user'] = request.user
        instance = vaccination_appointment.objects.create(**validated_data)
        instance.pet.set(pets)
        return instance



class test_booking_Serializer(serializers.ModelSerializer):
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(),
        many=True,
        write_only=True,
        source='pet'
    )
    pet = PetSerializer(many=True, read_only=True)

    class Meta:
        model = test_booking
        fields = [
            'id', 'pet', 'pet_ids',
            'test', 'test_id',
            'address', 'address_id',
            'date', 'payment_status', 'amount'
        ]
        read_only_fields = ['user', 'booking_id']

    def create(self, validated_data):
        request = self.context['request']
        pets = validated_data.pop('pet')
        validated_data['user'] = request.user
        instance = test_booking.objects.create(**validated_data)
        instance.pet.set(pets)
        return instance




from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import order, order_item


from daycare.serializers import *

class DayCareBookingSerializer(serializers.ModelSerializer):
    daycare = day_care_serializer(read_only=True)
    food_selection = food_menu_serializer(many=True, read_only=True)
    pets = PetSerializer(many=True, read_only=True)

    daycare_id = serializers.PrimaryKeyRelatedField(
        queryset=day_care.objects.all(), write_only=True, source='daycare'
    )
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True, source='pets'
    )
    food_selection_ids = serializers.PrimaryKeyRelatedField(
        queryset=food_menu.objects.all(), many=True, write_only=True, source='food_selection'
    )

    class Meta:
        model = day_care_booking
        fields = [
            'id', 'user',
            'daycare', 'daycare_id',
            'pets', 'pet_ids',
            'food_selection', 'food_selection_ids',
            'date_from', 'date_to',
            'half_day', 'full_day',
            'payment_status', 'total_cost', 'status'
        ]
        read_only_fields = [
            'id', 'user', 'daycare', 'pets', 'food_selection',
            'total_cost', 'payment_status', 'status', 'booking_id'
        ]

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("date_from must be before or equal to date_to")
        if date_from == date_to and data.get('half_day') and data.get('full_day'):
            raise serializers.ValidationError("Can't select both half-day and full-day on same day.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        pets = validated_data.pop('pets', [])
        food_items = validated_data.pop('food_selection', [])
        daycare = validated_data.pop('daycare')
        validated_data['user'] = request.user

        booking = day_care_booking.objects.create(daycare=daycare, **validated_data)
        booking.pets.set(pets)
        booking.food_selection.set(food_items)
        booking.save()
        return booking



from serviceprovider.serializer import *

class service_booking_Serializer(serializers.ModelSerializer):
    
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(),
        many=True,
        write_only=True,
        source='pets'
    )

    pets = PetSerializer(many=True, read_only=True)

    service_provider = serializers.PrimaryKeyRelatedField(
        queryset=service_provider.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    services_details = service_serializer(source='services', many=True, read_only=True)
    service_provider_details = service_provider_serializer(source='service_provider', read_only=True)

    address_id = serializers.PrimaryKeyRelatedField(
        queryset=customer_address.objects.all(), write_only=True, source="address"
    )
    address = customer_address_serializer(read_only=True)

    class Meta:
        model = service_booking
        fields = [
            'id',
            'user',
            'service_provider', 'service_provider_details',
            'services_id', 'services_details',
            'pets', 'pet_ids',
            'date',
            'address', 'address_id',
            'at_home',
            'payment_status'
        ]
        read_only_fields = ['user', 'booking_id', 'service_provider_details', 'services_details']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)



class OrderItemSerializer(serializers.ModelSerializer):
    
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all())
    product_details = product_category_serializer(source='product', read_only=True)

    class Meta:
        model = order_item
        fields = ['product', 'quantity', 'product_details']



class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True)
    
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=customer_address.objects.all(), write_only=True, source="address"
    )

    # Read-only nested serializers
    address = customer_address_serializer(read_only=True)  # <== Add this
   
    class Meta:
        model = order
        fields = ['id', 'user', 'total', 'address', 'address_id', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order_instance = order.objects.create(user=self.context['request'].user, **validated_data)

        for item_data in items_data:
            order_item.objects.create(order=order_instance, **item_data)

        return order_instance
    


class PastVaccinationSerializer(serializers.ModelSerializer):
    
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(),
        write_only=True,
        source='pet'
    )

    # Read-only nested pet details
    pet = PetSerializer(read_only=True)

    class Meta:
        model = PastVaccination
        fields = ['id', 'name', 'report', 'pet_id', 'pet', 'uploaded_at']
        read_only_fields = ['uploaded_at']
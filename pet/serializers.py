from rest_framework import serializers
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
    

from doctor.serializer import *
from masters.serializers import *
    
class consultation_appointment_Serializer(serializers.ModelSerializer):
    
   

    pet = PetSerializer(many=True, read_only=True)
    symptom = symptom_serializer(many=True, read_only=True)
    doctor = doctor_serializer(read_only=True)

    class Meta:
        model = consultation_appointment
        fields = ['id', 'pet', 'symptom', 'doctor', 'date', 'is_online', 'payment_status']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    

from doctor.serializer import *
from masters.serializers import *

class vaccination_appointment_Serializer(serializers.ModelSerializer):
    
    pet = PetSerializer(many=True)  # Use the PetSerializer to include all pet details
    vaccination = vaccination_serializer(many=True)  # Use the VaccinationSerializer to include all vaccination details
    doctor = doctor_serializer() 

    class Meta:
        model = vaccination_appointment
        fields = ['id', 'pet', 'vaccination', 'doctor', 'date', 'payment_status']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)

class test_booking_Serializer(serializers.ModelSerializer):
    

    test = test_serializer(many=True)
    pet = PetSerializer(many=True)  # Use the PetSerializer to include all pet details
    doctor = doctor_serializer() 


    class Meta:
        model = test_booking
        fields = ['id', 'pet', 'test', 'doctor', 'date', 'payment_status', 'report']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
    

from masters.serializers import *

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType



class CartSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(write_only=True)  # e.g., "product", "vaccination"
    object_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = cart
        fields = ['item_type', 'object_id', 'quantity']

    def validate(self, data):
        model = data['item_type'].lower()
        try:
            content_type = ContentType.objects.get(model=model)
            model_class = content_type.model_class()
            model_class.objects.get(id=data['object_id'])  # Ensure object exists
            data['content_type'] = content_type
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(f"No model named '{model}' exists.")
        except model_class.DoesNotExist:
            raise serializers.ValidationError(f"{model.title()} with ID {data['object_id']} not found.")
        return data

    def create(self, validated_data):
        return cart.objects.create(
            user=self.context['request'].user,
            content_type=validated_data['content_type'],
            object_id=validated_data['object_id'],
            quantity=validated_data['quantity']
        )

class AddToCartSerializer(serializers.Serializer):
    item_type = serializers.ChoiceField(choices=['product', 'service', 'vaccination', 'test'])
    object_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)




from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import order, order_item

class OrderItemSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)
    item = serializers.SerializerMethodField()

    class Meta:
        model = order_item
        fields = ['item_type', 'object_id', 'quantity', 'item']

    def get_item(self, obj):
        return str(obj.content_object)

    def validate(self, data):
        try:
            content_type = ContentType.objects.get(model=data['item_type'].lower())
            model_class = content_type.model_class()
            model_class.objects.get(id=data['object_id'])  # ensure object exists
            data['content_type'] = content_type
        except Exception:
            raise serializers.ValidationError("Invalid item_type or object_id")
        return data

    def create(self, validated_data):
        return order_item.objects.create(
            order=self.context['order'],
            content_type=validated_data['content_type'],
            object_id=validated_data['object_id'],
            quantity=validated_data['quantity']
        )


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
            serializer = OrderItemSerializer(data=item_data, context={'order': order_instance})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return order_instance



from daycare.serializers import *

class DayCareBookingSerializer(serializers.ModelSerializer):
    
    daycare = day_care_serializer(read_only=True)
    pets = PetSerializer(many=True, read_only=True)

    # For creating
    daycare_id = serializers.PrimaryKeyRelatedField(
        queryset=day_care.objects.all(), write_only=True, source='daycare'
    )
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=pet.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = day_care_booking
        fields = [
            'id', 'user', 'daycare', 'daycare_id',
            'pets', 'pet_ids', 'date_from', 'date_to',
            'drop_off', 'pick_up', 'food_selection', 'payment_status',
            'half_day_on_checkin', 'half_day_on_checkout', 'total_cost'
        ]
        read_only_fields = ['id', 'user', 'daycare', 'pets', 'total_cost', 'payment_status']

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        half_in = data.get('half_day_on_checkin', False)
        half_out = data.get('half_day_on_checkout', False)

        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("date_from must be before or equal to date_to")

        if date_from == date_to and half_in and half_out:
            raise serializers.ValidationError("Can't select both half-day check-in and check-out on same day.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        pets = validated_data.pop('pet_ids', [])
        daycare = validated_data.pop('daycare')

        validated_data['user'] = user

        booking = day_care_booking.objects.create(daycare=daycare, **validated_data)
        booking.pets.set(pets)
        booking.total_cost = self.calculate_total_cost(booking)
        booking.save()

        return booking

    def calculate_total_cost(self, booking):
        days = (booking.date_to - booking.date_from).days + 1
        if booking.half_day_on_checkin:
            days -= 0.5
        if booking.half_day_on_checkout:
            days -= 0.5
        return round(float(booking.daycare.price_per_day) * days, 2)



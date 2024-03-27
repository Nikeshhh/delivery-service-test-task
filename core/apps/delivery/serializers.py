from rest_framework import serializers
from core.apps.delivery.models import Cargo, Location


class CreateCargoSerializer(serializers.ModelSerializer):
    pick_up_zip = serializers.CharField()
    delivery_zip = serializers.CharField()

    class Meta:
        model = Cargo
        fields = ('pick_up_zip', 'delivery_zip', 'weight', 'description')

    def create(self, validated_data):
        return Cargo.objects.create(
            pick_up_location=Location.objects.get(zip_code=validated_data.get('pick_up_zip')),
            delivery_location=Location.objects.get(zip_code=validated_data.get('delivery_zip')),
            weight=validated_data.get('weight'),
            description=validated_data.get('description')
        )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'city',
            'state',
            'zip_code',
            'latitude',
            'longitude'
        )


class ListCargoSerializer(serializers.Serializer):
    pick_up_location = LocationSerializer()
    delivery_location = LocationSerializer()
    car_count = serializers.IntegerField()


class DeliveryCarSerializer(serializers.Serializer):
    car_number = serializers.CharField()
    distance = serializers.FloatField()


class RetreiveCargoSerializer(serializers.Serializer):
    pick_up_location = LocationSerializer()
    delivery_location = LocationSerializer()
    weight = serializers.IntegerField()
    description = serializers.CharField()
    cars = DeliveryCarSerializer(many=True)


class EditDeliveryCarSerializer(serializers.Serializer):
    ...
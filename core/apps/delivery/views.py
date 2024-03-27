from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from core.apps.delivery.models import Cargo, DeliveryCar
from core.apps.delivery.serializers import (
    CreateCargoSerializer,
    EditCargoSerializer,
    EditDeliveryCarSerializer,
    ListCargoSerializer,
    RetreiveCargoSerializer,
    RetrieveDeliveryCarSerializer
)
from core.apps.delivery.services import calculate_distance


class CargoViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cargo.objects.select_related()

    def get_queryset(self):
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCargoSerializer
        elif self.action == 'list':
            return ListCargoSerializer
        elif self.action == 'retrieve':
            return RetreiveCargoSerializer
        elif self.action in ('update', 'partial_update'):
            return EditCargoSerializer
        
    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, HTTP_201_CREATED)
        else:
            return Response({'success': False, 'errors': serializer.errors}, HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cars_queryset = DeliveryCar.objects\
            .select_related('current_location')\
            .only('current_location', 'car_number')
        for car in cars_queryset:
            car.distance = calculate_distance(car.current_location, instance.pick_up_location)
        instance.cars = cars_queryset
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request: HttpRequest, *args, **kwargs):
        cargo_queryset = Cargo.objects.select_related()
        cars_queryset = DeliveryCar.objects.select_related()
        for cargo in cargo_queryset:
            cargo.car_count = len(list(filter(
                lambda x: calculate_distance(x.current_location, cargo.pick_up_location) < 450,
                cars_queryset
            )))
        cargo_serializer = self.get_serializer(cargo_queryset, many=True)
        return Response(cargo_serializer.data)


class DeliveryCarViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = DeliveryCar.objects.select_related()
    serializer_class = RetrieveDeliveryCarSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return EditDeliveryCarSerializer
        return super().get_serializer_class()
    
    def partial_update(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response({'success': False, 'errors': serializer.errors}, HTTP_400_BAD_REQUEST)
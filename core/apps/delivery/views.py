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
from drf_spectacular.utils import extend_schema, OpenApiParameter


class CargoViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cargo.objects\
        .select_related('pick_up_location', 'delivery_location')

    def get_queryset(self):
        return super().get_queryset()
    
    def filter_queryset(self, queryset):
        if self.action == 'list':
            if max_weight := self.request.query_params.get('max_weight'):
                print(max_weight)
                return queryset.filter(weight__lte=max_weight)
        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCargoSerializer
        elif self.action == 'list':
            return ListCargoSerializer
        elif self.action == 'retrieve':
            return RetreiveCargoSerializer
        elif self.action in ('update', 'partial_update'):
            return EditCargoSerializer
        
    @extend_schema(summary='Создать груз')
    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, HTTP_201_CREATED)
        else:
            return Response({'success': False, 'errors': serializer.errors}, HTTP_400_BAD_REQUEST)
        
    @extend_schema(summary='Получить посылку по ID')
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        cars_queryset = DeliveryCar.objects\
            .select_related('current_location')\
            .only('current_location', 'car_number')
        
        # Расчет расстояния от каждой машины
        for car in cars_queryset:
            car.distance = calculate_distance(car.current_location, instance.pick_up_location)
        instance.cars = cars_queryset

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
            summary='Получить список грузов',
            parameters=[
                OpenApiParameter(name='max_weight',
                                description='Отфильтровать по весу', required=False, type=str),
                OpenApiParameter(name='max_distance', 
                                description='Отфильтровать машины по дистанции', required=False, type=str),
            ]
    )
    def list(self, request: HttpRequest, *args, **kwargs):
        """
        Получение списка грузов.
        :param: max_distance - отбирает только такие машины, расстояние до которых < max_distance
        :param: max_weight - отбирает толькое такие грузы, вес которых < max_weight
        """
        cargo_queryset = self.filter_queryset(self.get_queryset())
        cars_queryset = DeliveryCar.objects.select_related('current_location')

        # Начальное значение параментра max_distance
        max_distance = request.query_params.get('max_distance')
        if max_distance:
            max_distance = int(max_distance)
        else:
            max_distance = 450
            
        for cargo in cargo_queryset:
            # Рассчет количества машин
            cargo.car_count = len(list(filter(
                lambda car: 
                calculate_distance(car.current_location, cargo.pick_up_location) < max_distance and
                                                                        car.capacity >= cargo.weight,
                cars_queryset
            )))
        cargo_serializer = self.get_serializer(cargo_queryset, many=True)
        return Response(cargo_serializer.data)
    
    @extend_schema(summary='Редактировать груз по ID')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(summary='Редактировать груз по ID (patch)')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(summary='Удалить груз по ID')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DeliveryCarViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = DeliveryCar.objects.select_related('current_location')
    serializer_class = RetrieveDeliveryCarSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return EditDeliveryCarSerializer
        return super().get_serializer_class()
    
    @extend_schema(summary='Получить список машин')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(summary='Получить данные о машине по ID')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(summary='Обновить локацию машины по ZIP коду')
    def partial_update(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response({'success': False, 'errors': serializer.errors}, HTTP_400_BAD_REQUEST)

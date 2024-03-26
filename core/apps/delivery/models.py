from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from random import choice


class Location(models.Model):
    city = models.CharField(
        verbose_name='Название города',
        max_length=255
    )
    state = models.CharField(
        verbose_name='Название штата',
        max_length=255
    )
    zip_code = models.CharField(
        verbose_name='Почтовый индекс (zip)'
    )
    latitude = models.FloatField(
        verbose_name='Широта',
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
        validators=[MaxValueValidator(180), MinValueValidator(-180)]
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self) -> str:
        return f'{self.state}:{self.city} ({self.longitude}, {self.latitude})'
    
    @classmethod
    def get_random_location(cls) -> 'Location':
        return choice(cls.objects.all())
    

class Cargo(models.Model):
    pick_up_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT, # Мое решение: нельзя удалять локацию, пока к ней привязаны грузы
        verbose_name='Локация подбора',
        related_name='pick_ups'
    )
    delivery_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT, # Мое решение: нельзя удалять локацию, пока к ней привязаны грузы
        verbose_name='Локация доставки',
        related_name='deliveries'
    )
    weight = models.IntegerField(
        verbose_name='Вес груза',
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )
    description = models.TextField(
        verbose_name='Описание груза'
    )

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'

    def __str__(self) -> str:
        return f'{self.pick_up_location} -> {self.delivery_location} : {self.weight}'


class DeliveryCar(models.Model):
    car_number = models.CharField(
        verbose_name='Уникальный номер',
        max_length=5,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{4}[A-Z]$')]
    )
    current_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT, # Мое решение: нельзя удалить локацию, пока в ней есть машина
        verbose_name='Текущая локация',
        default=Location.get_random_location,
        related_name='cars'
    )
    capacity = models.IntegerField(
        verbose_name='Грузоподъемность',
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self) -> str:
        return f'{self.car_number}:{self.capacity} Сейчас в {self.current_location}'
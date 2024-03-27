from rest_framework.test import APIClient
import pytest

from core.apps.delivery.models import Cargo, DeliveryCar, Location

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def create_locations():
    Location.objects.create(
        city='New York',
        state='New York',
        zip_code='10029',
        latitude=40.79265,
        longitude=-73.94788
    )
    Location.objects.create(
        city='New York',
        state='New York',
        zip_code='10024',
        latitude=40.78534,
        longitude=-73.97138
    )
    Location.objects.create(
        city='New York',
        state='New York',
        zip_code='10014',
        latitude=40.73407,
        longitude=-74.00601
    )
    Location.objects.create(
        city='Very very far',
        state='Far away',
        zip_code='99999',
        latitude=0,
        longitude=0
    )


@pytest.fixture
def cargos():
    loc1 = Location.objects.get(zip_code='10029')
    loc2 = Location.objects.get(zip_code='10024')
    cargo1 = Cargo.objects.create(
        pick_up_location=loc1,
        delivery_location=loc2,
        weight=555,
        description='very nice cargo'
    )
    cargo2 = Cargo.objects.create(
        pick_up_location=loc2,
        delivery_location=loc1,
        weight=555,
        description='very nice cargo2'
    )
    return [cargo1, cargo2]


@pytest.fixture
def create_cars():
    car = DeliveryCar.objects.create(
        car_number='1234F',
        current_location=Location.objects.get(zip_code='10024'),
        capacity=1000
    )
    car2 = DeliveryCar.objects.create(
        car_number='1234E',
        current_location=Location.objects.get(zip_code='10029'),
        capacity=1000
    )
    far_away_car = DeliveryCar.objects.create(
        car_number='1234D',
        current_location=Location.objects.get(zip_code='99999'),
        capacity=1000
    )
    return [car, car2, far_away_car]
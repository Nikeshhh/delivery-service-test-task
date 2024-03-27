from django.urls import reverse
import pytest

from core.apps.delivery.models import Cargo, DeliveryCar, Location


@pytest.mark.django_db
def test_create_new_cargo(client):
    # 10029 -> 10024
    url = reverse('cargo-list')
    cargo_data = {
        'pick_up_zip': '10029',
        'delivery_zip': '10024',
        'weight': 555,
        'description': 'very nice cargo'
    }
    response = client.post(url, cargo_data)

    assert response.status_code == 201, response.data
    assert Cargo.objects.count() == 1
    obj = Cargo.objects.first()
    
    assert obj.weight == 555
    assert obj.description == 'very nice cargo'
    assert obj.pick_up_location.zip_code == '10029'
    assert obj.delivery_location.zip_code == '10024'


@pytest.mark.django_db
def test_cargo_list_correct_cars(client, create_cargos, create_cars):
    url = reverse('cargo-list')
    response = client.get(url)

    assert response.data[0].get('car_count') == 2
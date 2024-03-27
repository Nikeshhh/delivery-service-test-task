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
def test_cargo_list_correct_cars(client, cargos, create_cars):
    url = reverse('cargo-list')
    response = client.get(url)

    assert response.data[0].get('car_count') == 2


@pytest.mark.django_db
def test_delivery_car_location_update(client, create_cars):
    url = reverse('car-detail', args=(create_cars[0].pk, ))
    response = client.patch(url, {'zip_code': '99999'})

    assert response.status_code == 200
    create_cars[0].refresh_from_db()
    assert create_cars[0].current_location.zip_code == '99999'


@pytest.mark.django_db
def test_cargo_update(client, cargos):
    url = reverse('cargo-detail', args=(cargos[0].pk,))
    update_data = {
        'weight': 666,
        'description': 'new desc'
    }

    response = client.put(url, update_data)

    assert response.status_code == 200

    cargos[0].refresh_from_db()
    assert cargos[0].weight == 666
    assert cargos[0].description == 'new desc'


@pytest.mark.django_db
def test_cargo_partial_update(client, cargos):
    url = reverse('cargo-detail', args=(cargos[0].pk,))
    update_data = {
        'weight': 666,
    }

    response = client.patch(url, update_data)

    assert response.status_code == 200

    cargos[0].refresh_from_db()
    assert cargos[0].weight == 666


@pytest.mark.django_db
def test_cargo_delete(client, cargos):
    url = reverse('cargo-detail', args=(cargos[0].pk,))

    response = client.delete(url)

    assert response.status_code == 204

    assert Cargo.objects.count() == 1
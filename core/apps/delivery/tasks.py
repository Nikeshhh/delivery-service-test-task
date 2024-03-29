from celery import shared_task
from django.db.transaction import atomic
from core.apps.delivery.models import DeliveryCar


@shared_task()
def update_locations():
    with atomic():
        for car in DeliveryCar.objects.select_for_update():
            car.set_random_location()
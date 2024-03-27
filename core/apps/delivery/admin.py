from django.contrib import admin

from core.apps.delivery.models import Cargo, DeliveryCar, Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('city', 'state')


@admin.register(DeliveryCar)
class DeliveryCarAdmin(admin.ModelAdmin):
    raw_id_fields = ('current_location', )

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    raw_id_fields = ('pick_up_location', 'delivery_location')
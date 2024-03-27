from rest_framework.routers import DefaultRouter

from core.apps.delivery.views import CargoViewSet, DeliveryCarViewSet

router = DefaultRouter()

router.register('cargo', CargoViewSet, 'cargo')
router.register('car', DeliveryCarViewSet, 'car')

urlpatterns = [

] + router.urls

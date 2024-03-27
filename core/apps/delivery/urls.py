from rest_framework.routers import DefaultRouter

from core.apps.delivery.views import CargoViewSet

router = DefaultRouter()

router.register('cargo', CargoViewSet, 'cargo')

urlpatterns = [

] + router.urls

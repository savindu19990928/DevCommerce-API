from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet, SerialNumberViewSet

router = DefaultRouter()
router.register(r'movements', StockMovementViewSet, basename='stockmovement')
router.register(r'serials', SerialNumberViewSet, basename='serialnumber')

urlpatterns = [
    path('', include(router.urls)),
]

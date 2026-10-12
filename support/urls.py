from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerCareCaseViewSet, CommunicationHistoryViewSet

router = DefaultRouter()
router.register(r'cases', CustomerCareCaseViewSet, basename='customercarecase')
router.register(r'communications', CommunicationHistoryViewSet, basename='communicationhistory')

urlpatterns = [
    path('', include(router.urls)),
]

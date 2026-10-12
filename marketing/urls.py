from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationTagViewSet

router = DefaultRouter()
router.register(r'tags', RecommendationTagViewSet, basename='recommendationtag')

urlpatterns = [
    path('', include(router.urls)),
]

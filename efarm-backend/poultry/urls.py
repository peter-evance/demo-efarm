from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'poultry'

router = routers.DefaultRouter()
router.register(r'flock-sources', FlockSourceViewSet, basename='flock-sources')
router.register(r'flocks', FlockViewSet, basename='flocks')
router.register(r'flock-histories', FlockHistoryViewSet, basename='flock-histories')
router.register(r'housing-structures', HousingStructureViewSet, basename='housing-structures')

urlpatterns = [
    path('', include(router.urls)),
]

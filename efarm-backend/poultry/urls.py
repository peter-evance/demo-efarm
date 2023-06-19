from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'poultry'

router = routers.DefaultRouter()
router.register(r'flock-sources', FlockSourceViewSet, basename='flock-sources')
router.register(r'flocks', FlockViewSet, basename='flocks')
router.register(r'flock-breeds', FlockBreedViewSet, basename='flock-breeds')
router.register(r'flock-breed-information', FlockBreedInformationViewSet, basename='flock-breed-information')
router.register(r'egg-collection', EggCollectionViewSet, basename='egg-collection')
router.register(r'flock-histories', FlockHistoryViewSet, basename='flock-histories')
router.register(r'housing-structures', HousingStructureViewSet, basename='housing-structures')
router.register(r'flock-movements', FlockMovementViewSet, basename='flock-movements')
router.register(r'flock-inspection-records', FlockInspectionRecordViewSet, basename='flock-inspection-records')

urlpatterns = [
    path('', include(router.urls)),
]

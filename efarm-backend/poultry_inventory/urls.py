from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'poultry_inventory'

router = routers.DefaultRouter()
router.register(r'flock-inventories', FlockInventoryViewSet, basename='flock-inventories')
router.register(r'flock-inventory-histories', FlockInventoryHistoryViewSet, basename='flock-inventory-histories')

urlpatterns = [
    path('', include(router.urls)),

]

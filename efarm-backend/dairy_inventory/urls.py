from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'dairy_inventory'

router = routers.DefaultRouter()
router.register(r'milk', MilkInventoryViewSet, basename='milk-dairy_inventory')
router.register(r'milk-dairy_inventory-update-history', MilkInventoryUpdateHistoryViewSet)
router.register(r'cows-inventory', CowInventoryViewSet, basename='cows-inventory')
router.register(r'cows-inventory-history', CowInventoryUpdateHistoryViewSet, basename='cow-inventory-history')
router.register(r'cows-pen-inventory', CowPenInventoryViewSet, basename='cow-pen-inventory')
router.register(r'cows-pen-history', CowPenHistoryViewSet, basename='cow-pen-history')
router.register(r'barn-inventory-cows', BarnInventoryViewSet, basename='barn-inventory-cows')
router.register(r'barn-inventory-cows-history', BarnInventoryHistoryViewSet, basename='barn-inventory-cows-history')

urlpatterns = [
    path('', include(router.urls)),
]

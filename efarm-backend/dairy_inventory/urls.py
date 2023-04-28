from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'milk-inventory', views.MilkInventoryViewSet, basename='milk-inventory')
router.register(r'milk-inventory-update-history', views.MilkInventoryUpdateHistoryViewSet,
                basename='milk-inventory-update-history')

urlpatterns = [
    path('', include(router.urls)),
]

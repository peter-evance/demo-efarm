from rest_framework import viewsets
from .serializers import *


class MilkInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MilkInventory.objects.all()
    serializer_class = MilkInventorySerializer


class MilkInventoryUpdateHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MilkInventoryUpdateHistory.objects.all()
    serializer_class = MilkInventoryUpdateHistorySerializer

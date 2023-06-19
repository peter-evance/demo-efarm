from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from .serializers import *


class MilkInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MilkInventory.objects.all()
    serializer_class = MilkInventorySerializer


class MilkInventoryUpdateHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MilkInventoryUpdateHistory.objects.all()
    serializer_class = MilkInventoryUpdateHistorySerializer


class CowInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the CowInventory model.

    Provides the following action:
    - `retrieve`: Retrieves cow inventory record.

    """

    queryset = CowInventory.objects.all()
    serializer_class = CowInventorySerializer

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')


class CowInventoryUpdateHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the CowInventoryUpdateHistory model.

    Provides the following actions:
    - `list`: Retrieves a list of all cow inventory update histories.
    - `retrieve`: Retrieves a specific cow inventory update history by its ID.

    """

    queryset = CowInventoryUpdateHistory.objects.all()
    serializer_class = CowInventoryUpdateHistorySerializer


class CowPenInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the CowPenInventory model.

    Provides the following actions:
    - `list`: Retrieves a list of all cow pen inventories.
    - `retrieve`: Retrieves a specific cow pen inventory by its ID.

    """

    queryset = CowPenInventory.objects.all()
    serializer_class = CowPenInventorySerializer


class CowPenHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the CowPenHistory model.

    Provides the following actions:
    - `list`: Retrieves a list of all cow pen histories.
    - `retrieve`: Retrieves a specific cow pen history by its ID.

    """

    queryset = CowPenHistory.objects.all()
    serializer_class = CowPenHistorySerializer


class BarnInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the BarnInventory model.

    Provides the following actions:
    - `list`: Retrieves a list of all barn inventories.
    - `retrieve`: Retrieves a specific barn inventory by its ID.

    """

    queryset = BarnInventory.objects.all()
    serializer_class = BarnInventorySerializer


class BarnInventoryHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the BarnInventoryHistory model.

    Provides the following actions:
    - `list`: Retrieves a list of all barn inventory histories.
    - `retrieve`: Retrieves a specific barn inventory history by its ID.

    """

    queryset = BarnInventoryHistory.objects.all()
    serializer_class = BarnInventoryHistorySerializer

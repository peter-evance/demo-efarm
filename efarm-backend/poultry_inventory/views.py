from rest_framework import viewsets

from .serializers import *


class FlockInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving FlockInventory instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock inventories.
    - `retrieve`: Retrieves a specific flock inventory by its ID.

    """
    queryset = FlockInventory.objects.all()
    serializer_class = FlockInventorySerializer


class FlockInventoryHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving FlockInventoryHistory instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock inventory histories.
    - `retrieve`: Retrieves a specific flock inventory history by its ID.

    """
    queryset = FlockInventoryHistory.objects.all()
    serializer_class = FlockInventoryHistorySerializer

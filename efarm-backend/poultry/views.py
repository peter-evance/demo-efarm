from rest_framework import viewsets, status
from rest_framework.response import Response

from poultry.serializers import *


class FlockSourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FlockSource instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock sources.
    - `create`: Creates a new flock source.
    - `retrieve`: Retrieves a specific flock source by its ID.
    - `update`: Updates a flock source.
    - `destroy`: Deletes a flock source.

    """
    queryset = FlockSource.objects.all()
    serializer_class = FlockSourceSerializer


class FlockBreedViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FlockBreed instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock breeds.
    - `create`: Creates a new flock breeds.
    - `retrieve`: Retrieves a specific flock breed by its ID.
    - `update`: Updates a flock breeds.
    - `destroy`: Deletes a flock breeds.

    """
    queryset = FlockBreed.objects.all()
    serializer_class = FlockBreedSerializer


class HousingStructureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing HousingStructure instances.

    Provides the following actions:
    - `list`: Retrieves a list of all housing structures.
    - `create`: Creates a new housing structure.
    - `retrieve`: Retrieves a specific housing structure by its ID.
    - `update`: Updates a housing structure.
    - `destroy`: Deletes a housing structure.

    """
    queryset = HousingStructure.objects.all()
    serializer_class = HousingStructureSerializer


class FlockViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Flock instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flocks.
    - `create`: Creates a new flock.
    - `retrieve`: Retrieves a specific flock by its ID.
    - `update`: Updates a flock.
    - `destroy`: Deletes a flock.

    Additionally, it overrides the 'update' method to check if the 'chicken_type'
    field is included in the update data and returns an error response if it is.

    """
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer

    def update(self, request, *args, **kwargs):
        """
        Updates a Flock instance.

        Parameters:
        - `request`: The HTTP request object.
        - `args`: Additional arguments passed to the view.
        - `Kwargs`: Additional keyword arguments passed to the view.

        Returns:
        - A response with the updated serialized data or an error response.

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if 'chicken_type' in request.data:
            new_chicken_type = request.data['chicken_type']
            if new_chicken_type != instance.chicken_type:
                return Response({"error": "Cannot update the chicken_type"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class FlockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving FlockHistory instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock histories.
    - `retrieve`: Retrieves a specific flock history by its ID.

    """
    queryset = FlockHistory.objects.all()
    serializer_class = FlockHistorySerializer


class FlockMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FlockMovement instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock movements.
    - `create`: Creates a new flock movement.
    - `retrieve`: Retrieves a specific flock movement by its ID.
    - `update`: Updates a flock movement.
    - `destroy`: Deletes a flock movement.

    """
    queryset = FlockMovement.objects.all()
    serializer_class = FlockMovementSerializer


class FlockInspectionRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FlockInspectionRecord instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock inspection records.
    - `create`: Creates a new flock inspection record.
    - `retrieve`: Retrieves a specific flock inspection record by its ID.
    - `update`: Updates a flock inspection record.
    - `destroy`: Deletes a flock inspection record.

    """
    queryset = FlockInspectionRecord.objects.all()
    serializer_class = FlockInspectionRecordSerializer


class FlockBreedInformationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FlockBreedInformation instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock breed information.
    - `create`: Creates new flock breed information.
    - `retrieve`: Retrieves specific flock breed information by its ID.
    - `update`: Updates flock breed information.
    - `destroy`: Deletes flock breed information.

    """
    queryset = FlockBreedInformation.objects.all()
    serializer_class = FlockBreedInformationSerializer


class EggCollectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing EggCollection instances.

    Provides the following actions:

    list: Retrieve a list of all egg collections.

    create: Create a new egg collection.

    retrieve: Retrieves a specific egg collection by its ID.

    update: Updates an egg collection.

    destroy: Delete an egg collection.

    """

    queryset = EggCollection.objects.all()
    serializer_class = EggCollectionSerializer

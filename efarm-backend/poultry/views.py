from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response

from poultry.filters import *
from poultry.permissions import *
from poultry.serializers import *


class FlockSourceViewSet(viewsets.ModelViewSet):
    queryset = FlockSource.objects.all()
    serializer_class = FlockSourceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockSourceFilterSet
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create"]:
            # Only farm owner and farm manager should be allowed to create flock sources
            permission_classes = [CanAddFlockSource]
        elif self.action in ["destroy"]:
            # Only farm owner and farm manager should be allowed to delete flock sources
            permission_classes = [CanDeleteFlockSource]
        else:
            # For viewing flock sources, allow farm owner, farm manager, assistant farm manager, team leader,
            # and farm worker
            permission_classes = [CanViewFlockSource]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        # Disallow update for flock sources since the source is selected from choices
        return Response(
            {"detail": "Updates are not allowed for flock sources."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching flock sources
                return Response(
                    {
                        "detail": "No flock source(s) found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no flock sources in the database
                return Response(
                    {"detail": "No flock sources found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FlockBreedViewSet(viewsets.ModelViewSet):
    queryset = FlockBreed.objects.all()
    serializer_class = FlockBreedSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockBreedFilterSet
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create"]:
            # Only farm owner and farm manager should be allowed to create flock breeds

            permission_classes = [CanAddFlockBreed]
        elif self.action in ["destroy"]:
            # Only farm owner and farm manager should be allowed to delete flock breeds
            permission_classes = [CanDeleteFlockBreed]
        else:
            # For viewing flock breeds, allow farm owner, farm manager, assistant farm manager, team leader,
            # and farm worker
            permission_classes = [CanViewFlockBreeds]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        # Disallow update for flock breed since the breed name is selected from choices
        return Response(
            {"detail": "Updates are not allowed for flock breeds."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching flock breeds
                return Response(
                    {"detail": "No flock breed(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no flock breeds in the database
                return Response(
                    {"detail": "No flock breeds found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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

        if "chicken_type" in request.data:
            new_chicken_type = request.data["chicken_type"]
            if new_chicken_type != instance.chicken_type:
                return Response(
                    {"error": "Cannot update the chicken_type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
    - `list`: Retrieve a list of all egg collections.
    - `create`: Create a new egg collection.
    - `retrieve`: Retrieves a specific egg collection by its ID.
    - `update`: Updates an egg collection.
    - `destroy`: Delete an egg collection.

    """

    queryset = EggCollection.objects.all()
    serializer_class = EggCollectionSerializer

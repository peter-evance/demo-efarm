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
        raise MethodNotAllowed("PUT")

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
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching flock breeds
                return Response(
                    {
                        "detail": "No flock breed(s) found matching the provided filters."
                    },
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
    queryset = HousingStructure.objects.all()
    serializer_class = HousingStructureSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HousingStructureFilterSet
    ordering_fields = ["house_type", "category"]
    permission_classes = [CanActOnHousingStructure]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching housing types
                return Response(
                    {"detail": "No Housing structure(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no housing structures in the database
                return Response(
                    {"detail": "No housing structure found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FlockViewSet(viewsets.ModelViewSet):
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockFilterSet
    ordering_fields = ["-date_established", "source"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [CanAddFlock]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [CanUpdateFlock]
        elif self.action in ["destroy"]:
            permission_classes = [CanDeleteFlock]
        else:
            permission_classes = [CanViewFlock]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching flocks
                return Response(
                    {"detail": "No flock(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no flock in the database
                return Response(
                    {"detail": "No flock found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FlockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlockHistory.objects.all()
    serializer_class = FlockHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockHistoryFilterSet
    ordering_fields = ["-date_changed", "flock", "rearing_method"]
    permission_classes = [CanActOnFlockHistory]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching flock history records.
                return Response(
                    {"detail": "No flock history found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no flock history in the database
                return Response(
                    {"detail": "No flock history available."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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

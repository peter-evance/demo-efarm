from rest_framework import viewsets, status
from rest_framework.response import Response

from poultry.models import *
from poultry.serializers import *


class FlockSourceViewSet(viewsets.ModelViewSet):
    queryset = FlockSource.objects.all()
    serializer_class = FlockSourceSerializer


class HousingStructureViewSet(viewsets.ModelViewSet):
    queryset = HousingStructure.objects.all()
    serializer_class = HousingStructureSerializer


class FlockViewSet(viewsets.ModelViewSet):
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Check if the 'chicken_type' field is included in the update data
        if 'chicken_type' in request.data:
            new_chicken_type = request.data['chicken_type']
            if new_chicken_type != instance.chicken_type:
                return Response({"error": "Cannot update the chicken_type"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class FlockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlockHistory.objects.all()
    serializer_class = FlockHistorySerializer

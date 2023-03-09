from rest_framework import viewsets
from rest_framework.response import Response

from .models import Cow
from .serializers import CowSerializer


class CowViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting cows.
    """
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

    def list(self, request):
        """
        Return a list of all cows.
        """
        queryset = self.get_queryset()
        serializer = CowSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new cow.
        """
        serializer = CowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        """
        Return the details of a single cow.
        """
        queryset = self.get_queryset()
        cow = queryset.get(pk=pk)
        serializer = CowSerializer(cow)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update the details of a single cow.
        """
        cow = Cow.objects.get(pk=pk)
        serializer = CowSerializer(cow, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """
        Delete a single cow.
        """
        cow = Cow.objects.get(pk=pk)
        cow.delete()
        return Response(status=204)



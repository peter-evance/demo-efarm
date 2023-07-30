from django_filters import rest_framework as filters

from dairy.models import *


class CowBreedFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CowBreed
        fields = ['name']
from django_filters import rest_framework as filters

from poultry.models import *


class CaseInsensitiveBooleanFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if value in ["true", "T", "t", "1"]:
            value = True
        elif value in ["false", "F", "f", "0"]:
            value = False
        return super().filter(qs, value)


class FlockSourceFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FlockSource
        fields = ["name"]


class FlockBreedFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FlockBreed
        fields = ["name"]
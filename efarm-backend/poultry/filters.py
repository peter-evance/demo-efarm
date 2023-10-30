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


class HousingStructureFilterSet(filters.FilterSet):
    housing_type = filters.CharFilter(lookup_expr="icontains")
    category = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = HousingStructure
        fields = ["housing_type", "category"]


class FlockFilterSet(filters.FilterSet):
    source = filters.CharFilter(lookup_expr="icontains")
    breed = filters.CharFilter(lookup_expr="icontains")
    chicken_type = filters.CharFilter(lookup_expr="icontains")
    is_present = CaseInsensitiveBooleanFilter(field_name="is_present")
    date_established = filters.DateFilter(
        field_name="date_established", lookup_expr="exact"
    )
    year_established = filters.NumberFilter(
        field_name="date_established__year", lookup_expr="exact"
    )
    month_established = filters.NumberFilter(
        field_name="date_established__month", lookup_expr="exact"
    )
    week_established = filters.NumberFilter(
        field_name="date_established__week", lookup_expr="exact"
    )
    day_established = filters.NumberFilter(
        field_name="date_established__day", lookup_expr="exact"
    )

    class Meta:
        model = Flock
        fields = [
            "source",
            "breed",
            "chicken_type",
            "date_established",
            "is_present",
            "year_established",
            "month_established",
            "week_established",
            "day_established",
        ]


class FlockHistoryFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    rearing_method = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FlockHistory
        fields = [
            "flock",
            "rearing_method"
        ]

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
        fields = ["flock", "rearing_method"]


class FlockMovementFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    from_structure = filters.CharFilter(lookup_expr="icontains")
    to_structure = filters.CharFilter(lookup_expr="icontains")
    year_of_movement = filters.NumberFilter(
        field_name="movement_date__year", lookup_expr="exact"
    )
    month_of_movement = filters.NumberFilter(
        field_name="movement_date__month", lookup_expr="exact"
    )
    week_of_movement = filters.NumberFilter(
        field_name="movement_date__week", lookup_expr="exact"
    )
    day_of_movement = filters.NumberFilter(
        field_name="movement_date__day", lookup_expr="exact"
    )

    class Meta:
        model = FlockMovement
        fields = [
            "flock",
            "from_structure",
            "to_structure",
            "year_of_movement",
            "month_of_movement",
            "week_of_movement",
            "day_of_movement",
        ]


class FlockInspectionRecordFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    month_of_inspection = filters.NumberFilter(
        field_name="date_of_inspection__month", lookup_expr="exact"
    )
    week_of_inspection = filters.NumberFilter(
        field_name="date_of_inspection__week", lookup_expr="exact"
    )
    day_of_inspection = filters.NumberFilter(
        field_name="date_of_inspection__day", lookup_expr="exact"
    )

    class Meta:
        model = FlockInspectionRecord
        fields = [
            "flock",
            "month_of_inspection",
            "week_of_inspection",
            "day_of_inspection",
        ]


class EggCollectionFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    month_of_collection = filters.NumberFilter(
        field_name="date_of_collection__month", lookup_expr="exact"
    )
    week_of_collection = filters.NumberFilter(
        field_name="date_of_collection__week", lookup_expr="exact"
    )
    day_of_collection = filters.NumberFilter(
        field_name="date_of_collection__day", lookup_expr="exact"
    )
    time_of_collection = filters.NumberFilter(
        field_name="time_of_collection__day", lookup_expr="exact"
    )

    class Meta:
        model = EggCollection
        fields = [
            "flock",
            "month_of_collection",
            "week_of_collection",
            "day_of_collection",
            "time_of_collection",
        ]

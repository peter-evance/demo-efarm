from django_filters import rest_framework as filters

from dairy.models import *


class CowBreedFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = CowBreed
        fields = ["name"]


class CaseInsensitiveBooleanFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if value in ["true", "T", "t", "1"]:
            value = True
        elif value in ["false", "F", "f", "0"]:
            value = False
        return super().filter(qs, value)


class CowFilterSet(filters.FilterSet):
    breed = filters.CharFilter(field_name="breed__name", lookup_expr="icontains")
    is_bought = CaseInsensitiveBooleanFilter(field_name="is_bought")
    gender = filters.CharFilter(field_name="gender", lookup_expr="exact")
    year_of_birth = filters.NumberFilter(
        field_name="date_of_birth__year", lookup_expr="exact"
    )
    month_of_birth = filters.NumberFilter(
        field_name="date_of_birth__month", lookup_expr="exact"
    )
    week_of_birth = filters.NumberFilter(
        field_name="date_of_birth__week", lookup_expr="exact"
    )
    day_of_birth = filters.NumberFilter(
        field_name="date_of_birth__day", lookup_expr="exact"
    )
    date_of_birth = filters.DateFilter(field_name="date_of_birth", lookup_expr="exact")
    availability_status = filters.CharFilter(
        field_name="availability_status", lookup_expr="icontains"
    )
    current_pregnancy_status = filters.CharFilter(
        field_name="current_pregnancy_status", lookup_expr="icontains"
    )
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")
    current_production_status = filters.CharFilter(
        field_name="current_production_status", lookup_expr="icontains"
    )
    tag_number = filters.CharFilter(field_name="tag_number", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Cow
        fields = [
            "breed",
            "is_bought",
            "gender",
            "year_of_birth",
            "month_of_birth",
            "week_of_birth",
            "day_of_birth",
            "date_of_birth",
            "availability_status",
            "current_pregnancy_status",
            "category",
            "current_production_status",
            "tag_number",
            "name",
        ]


class HeatFilterSet(filters.FilterSet):
    observation_time = filters.DateTimeFilter(
        field_name="observation_time", lookup_expr="exact"
    )

    class Meta:
        model = Heat
        fields = ["observation_time"]


class InseminatorFilterSet(filters.FilterSet):
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")

    class Meta:
        model = Inseminator
        fields = ["first_name", "last_name"]


class InseminationFilterSet(filters.FilterSet):
    cow = filters.CharFilter(field_name="cow__tag_number", lookup_expr="icontains")
    inseminator = filters.CharFilter(
        field_name="inseminator__first_name", lookup_expr="icontains"
    )
    success = CaseInsensitiveBooleanFilter(field_name="success")
    date_of_insemination = filters.DateTimeFilter(
        field_name="date_of_insemination", lookup_expr="exact"
    )
    year_of_insemination = filters.NumberFilter(
        field_name="date_of_insemination__year", lookup_expr="exact"
    )
    month_of_insemination = filters.NumberFilter(
        field_name="date_of_insemination__month", lookup_expr="exact"
    )
    week_of_insemination = filters.NumberFilter(
        field_name="date_of_insemination__week", lookup_expr="exact"
    )
    day_of_insemination = filters.NumberFilter(
        field_name="date_of_insemination__day", lookup_expr="exact"
    )

    class Meta:
        model = Insemination
        fields = ["cow", "success", "inseminator", "year_of_insemination", "month_of_insemination",
                  "week_of_insemination", "day_of_insemination"]


class PregnancyFilterSet(filters.FilterSet):
    cow = filters.CharFilter(field_name="cow__tag_number", lookup_expr="icontains")
    start_date = filters.DateFilter(field_name="start_date")
    year = filters.NumberFilter(field_name="start_date__year", lookup_expr="exact")
    month = filters.NumberFilter(field_name="start_date__month", lookup_expr="exact")
    pregnancy_failed_date = filters.DateFilter(field_name="pregnancy_failed_date")
    pregnancy_outcome = filters.CharFilter(
        field_name="pregnancy_outcome", lookup_expr="icontains"
    )
    pregnancy_status = filters.CharFilter(
        field_name="pregnancy_status", lookup_expr="icontains"
    )

    class Meta:
        model = Pregnancy
        fields = ["cow", "start_date", "year", "month", "pregnancy_failed_date", "pregnancy_outcome",
                  "pregnancy_status"]


class LactationFilterSet(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start_date")
    year = filters.NumberFilter(field_name="start_date__year", lookup_expr="exact")
    month = filters.NumberFilter(field_name="start_date__month", lookup_expr="exact")
    lactation_number = filters.NumberFilter(
        field_name="lactation_number", lookup_expr="exact"
    )

    class Meta:
        model = Lactation
        fields = ["start_date", "year", "month", "lactation_number"]


class MilkFilterSet(filters.FilterSet):
    cow = filters.CharFilter(field_name="cow__tag_number", lookup_expr="icontains")
    milking_date = filters.DateTimeFilter(field_name="milking_date")
    day_of_milking = filters.NumberFilter(
        field_name="milking_date__day", lookup_expr="exact"
    )
    week_of_milking = filters.NumberFilter(
        field_name="milking_date__week", lookup_expr="exact"
    )
    month_of_milking = filters.NumberFilter(
        field_name="milking_date__month", lookup_expr="exact"
    )
    year_of_milking = filters.NumberFilter(
        field_name="milking_date__year", lookup_expr="exact"
    )

    class Meta:
        model = Milk
        fields = ["cow", "milking_date", "day_of_milking", "week_of_milking", "month_of_milking",
                  "year_of_milking"]


class WeightRecordFilterSet(filters.FilterSet):
    cow = filters.CharFilter(field_name="cow__tag_number", lookup_expr="icontains")
    day_of_weighing = filters.NumberFilter(field_name="date__day", lookup_expr="exact")
    month_of_weighing = filters.NumberFilter(
        field_name="date__month", lookup_expr="exact"
    )
    year_of_weighing = filters.NumberFilter(
        field_name="date__year", lookup_expr="exact"
    )

    class Meta:
        model = WeightRecord
        fields = ["cow", "day_of_weighing", "month_of_weighing", "year_of_weighing"]


class CullingRecordFilterSet(filters.FilterSet):
    day_of_culling = filters.NumberFilter(field_name="date__day", lookup_expr="exact")
    month_of_culling = filters.NumberFilter(
        field_name="date__month", lookup_expr="exact"
    )
    year_of_culling = filters.NumberFilter(field_name="date__year", lookup_expr="exact")

    class Meta:
        model = CullingRecord
        fields = ["day_of_culling", "month_of_culling", "year_of_culling"]


class QuarantineRecordFilterSet(filters.FilterSet):
    reason = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = QuarantineRecord
        fields = ["reason"]

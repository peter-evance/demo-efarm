from django_filters import rest_framework as filters

from dairy.models import *


class CowBreedFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CowBreed
        fields = ['name']


class CaseInsensitiveBooleanFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if value in ['true', 'T', 't', '1']:
            value = True
        elif value in ['false', 'F', 'f', '0']:
            value = False
        return super().filter(qs, value)


class CowFilterSet(filters.FilterSet):
    breed = filters.CharFilter(field_name='breed__name', lookup_expr='icontains')
    is_bought = CaseInsensitiveBooleanFilter(field_name='is_bought')
    gender = filters.CharFilter(field_name='gender', lookup_expr='exact')
    year_of_birth = filters.NumberFilter(field_name='date_of_birth__year', lookup_expr='exact')
    month_of_birth = filters.NumberFilter(field_name='date_of_birth__month', lookup_expr='exact')
    week_of_birth = filters.NumberFilter(field_name='date_of_birth__week', lookup_expr='exact')
    day_of_birth = filters.NumberFilter(field_name='date_of_birth__day', lookup_expr='exact')
    date_of_birth = filters.DateFilter(field_name='date_of_birth', lookup_expr='exact')
    availability_status = filters.CharFilter(field_name='availability_status', lookup_expr='icontains')
    current_pregnancy_status = filters.CharFilter(field_name='current_pregnancy_status', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    current_production_status = filters.CharFilter(field_name='current_production_status', lookup_expr='icontains')
    tag_number = filters.CharFilter(field_name='tag_number', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Cow
        fields = ['breed', 'is_bought', 'gender', 'year_of_birth', 'month_of_birth', 'week_of_birth',
                  'day_of_birth', 'date_of_birth', 'availability_status', 'current_pregnancy_status',
                  'category', 'current_production_status', 'tag_number', 'name']

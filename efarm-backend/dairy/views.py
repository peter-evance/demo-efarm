import os

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse, Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from dairy.models import *
from dairy.serializers import *
from dairy.permissions import *
from dairy.filters import *


class CowBreedViewSet(viewsets.ModelViewSet):
    queryset = CowBreed.objects.all()
    serializer_class = CowBreedSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CowBreedFilterSet
    ordering_fields = ['name']

    def get_permissions(self):
        if self.action in ['create']:
            # Only farm owner and farm manager should be allowed to create cow breeds
            permission_classes = [CanAddCowBreed]
        elif self.action in ['destroy']:
            # Only farm owner and farm manager should be allowed to delete cow breeds
            permission_classes = [CanDeleteCowBreed]
        else:
            # For viewing cow breeds, allow farm owner, farm manager, assistant farm manager, team leader,
            # and farm worker
            permission_classes = [CanViewCowBreeds]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        # Disallow update for cow breeds since the name is selected from choices
        return Response({"detail": "Updates are not allowed for cow breeds."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching cow breeds
                return Response({"detail": "No cow breed(s) found matching the provided filters."},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                # If no query parameters are provided, and there are no cow breeds in the database
                return Response({"detail": "No cow breeds found in the farm yet."},
                                status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CowFilterSet
    ordering_fields = ['date_of_birth', 'name', 'gender', 'breed']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CanAddCow]
        elif self.action == 'destroy':
            permission_classes = [CanDeleteCow]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [CanUpdateCow]
        else:
            # For viewing cow breeds, allow farm owner, farm manager, assistant farm manager, team leader,
            # and farm worker
            permission_classes = [CanViewCow]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching cows
                return Response({"detail": "No cow(s) records found matching the provided filters."},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                # If no query parameters are provided, and there are no cows in the database
                return Response({"detail": "No cow records found in the farm yet."},
                                status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CowInBarnMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the CowInBarnMovement model.

    Provides the following actions:
    - `list`: Retrieves a list of all cow movements in the barn.
    - `retrieve`: Retrieves a specific cow movement by its ID.

    """
    serializer_class = CowInBarnMovementSerializer
    queryset = CowInBarnMovement.objects.all()


class CowInPenMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CowInPenMovement model.

    Provides the following actions:
    - `list`: Retrieves a list of all cow movements in the cow pens.
    - `retrieve`: Retrieves a specific cow movement by its ID.
    - `create`: Creates a new cow movement.
    - `update`: Updates an existing cow movement.
    - `partial_update`: Performs a partial update on an existing cow movement.
    - `destroy`: Deletes a specific cow movement.

    """
    serializer_class = CowInPenMovementSerializer
    queryset = CowInPenMovement.objects.all()


class CowPenViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CowPen model.

    Provides the following actions:
    - `list`: Retrieves a list of all cow pens.
    - `retrieve`: Retrieves a specific cow pen by its ID.
    - `create`: Creates a new cow pen.
    - `update`: Updates an existing cow pen.
    - `partial_update`: Performs a partial update on an existing cow pen.
    - `destroy`: Deletes a specific cow pen.

    """
    serializer_class = CowPenSerializer
    queryset = CowPen.objects.all()


class BarnViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Barn model.

    Provides the following actions:
    - `list`: Retrieves a list of all barns.
    - `retrieve`: Retrieves a specific barn by its ID.
    - `create`: Creates a new barn.
    - `update`: Updates an existing barn.
    - `partial_update`: Performs a partial update on an existing barn.
    - `destroy`: Deletes a specific barn.

    """
    serializer_class = BarnSerializer
    queryset = Barn.objects.all()


class MilkViewSet(viewsets.ModelViewSet):
    serializer_class = MilkSerializer
    queryset = Milk.objects.all()


class LactationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LactationSerializer
    queryset = Lactation.objects.all()


class PregnancyViewSet(viewsets.ModelViewSet):
    queryset = Pregnancy.objects.all()
    serializer_class = PregnancySerializer


class WeightRecordViewSet(viewsets.ModelViewSet):
    queryset = WeightRecord.objects.all()
    serializer_class = WeightRecordSerializer


class CullingViewSet(viewsets.ModelViewSet):
    queryset = Culling.objects.all()
    serializer_class = CullingSerializer


class MilkTodayView(APIView):
    def get(self, request, format=None):
        today = timezone.localdate()
        start_of_today = timezone.datetime.combine(today, timezone.datetime.min.time())
        end_of_today = timezone.datetime.combine(today, timezone.datetime.max.time())

        yesterday = today - timezone.timedelta(days=1)
        start_of_yesterday = timezone.datetime.combine(yesterday, timezone.datetime.min.time())
        end_of_yesterday = timezone.datetime.combine(yesterday, timezone.datetime.max.time())

        total_milk_today = \
            Milk.objects.filter(milking_date__range=(start_of_today, end_of_today)).aggregate(Sum('amount_in_kgs'))[
                'amount_in_kgs__sum'] or 0
        total_milk_yesterday = \
            Milk.objects.filter(milking_date__range=(start_of_yesterday, end_of_yesterday)).aggregate(
                Sum('amount_in_kgs'))[
                'amount_in_kgs__sum'] or 0

        milk_diff = total_milk_today - total_milk_yesterday
        percentage_difference = round((milk_diff / total_milk_yesterday) * 100 if total_milk_yesterday else 0, 2)

        return Response({'total_milk_today': total_milk_today,
                         'total_milk_yesterday': total_milk_yesterday,
                         'percentage_difference': percentage_difference})


class TotalAliveCowsView(APIView):
    def get(self, request, format=None):
        total_alive_cows = Cow.objects.filter(availability_status='Alive').values('id').distinct().count()
        return Response({'total_alive_cows': total_alive_cows})


class TotalAliveFemaleCowsView(APIView):
    def get(self, request, format=None):
        total_alive_female_cows = Cow.objects.filter(availability_status='Alive', gender='Female').values(
            'id').distinct().count()
        return Response({'total_alive_female_cows': total_alive_female_cows})


class TotalAliveMaleCowsView(APIView):
    def get(self, request, format=None):
        total_alive_male_cows = Cow.objects.filter(availability_status='Alive', gender='Male').values(
            'id').distinct().count()
        return Response({'total_alive_male_cows': total_alive_male_cows})


class CowsMilkedTodayView(APIView):
    def get(self, request, format=None):
        today = timezone.localdate()
        start_of_day = timezone.datetime.combine(today, timezone.datetime.min.time())
        end_of_day = timezone.datetime.combine(today, timezone.datetime.max.time())
        milking_cows = Milk.objects.filter(milking_date__range=(start_of_day, end_of_day)).values('cow_id').distinct()

        eligible_cows = Lactation.objects.filter(
            cow__gender='Male',
            end_date__isnull=True,
            pregnancy__isnull=True,
            start_date__lte=today,
        ).values_list('cow_id', flat=True)

        unmilked_cows = Cow.objects.filter(id__in=eligible_cows).exclude(id__in=milking_cows).count()
        milked_cows = milking_cows.count()

        return Response({
            'cows_milked_today': milked_cows,
            'cows_unmilked_today': unmilked_cows,
        })


class MilkProductionWeeklyView(APIView):
    def get(self, request, format=None):
        today = timezone.localdate()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=7)
        milk_records = Milk.objects.filter(milking_date__range=(start_of_week, end_of_week)).order_by('milking_date')

        # Create a dictionary to store the milk records grouped by day
        milk_production_data = {}
        for record in milk_records:
            day = record.milking_date.strftime('%A')
            if day not in milk_production_data:
                milk_production_data[day] = {'day': day, 'total_milk': record.amount_in_kgs}
            else:
                milk_production_data[day]['total_milk'] += record.amount_in_kgs
        milk_production_data = [{'day': day, 'milk_records': [record]} for day, record in milk_production_data.items()]

        return Response(milk_production_data)


class PregnantCowsView(APIView):
    def get(self, request, format=None):
        pregnancies_count = Pregnancy.objects.filter(pregnancy_status='Confirmed', date_of_calving__isnull=True).count()
        return Response({'pregnancies_count': pregnancies_count})


class LactatingCowsView(APIView):
    def get(self, request, format=None):
        lactating_cows = Lactation.objects.filter(end_date__isnull=True).values_list('cow__name', flat=True)
        lactating_cows_count = lactating_cows.count()
        return Response({'lactating_cows_count': lactating_cows_count, 'lactating_cows': lactating_cows})


def serve_carousel_images(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, 'dairy', 'carousels', filename)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='image/jpeg')

    else:
        Http404

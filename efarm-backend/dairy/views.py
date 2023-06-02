import os

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse, Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


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


class CowViewSet(viewsets.ModelViewSet):
    serializer_class = CowSerializer
    queryset = Cow.objects.all()


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

from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.views import APIView

from .models import *
from .serializers import *


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


class MilkViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting milk records.
    """
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer

    def list(self, request):
        """
        Return a list of all milk records.
        """
        queryset = self.get_queryset()
        serializer = MilkSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new milk record.
        """
        serializer = MilkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        """
        Return the details of a single milk record.
        """
        queryset = self.get_queryset()
        milk_record = queryset.get(pk=pk)
        serializer = MilkSerializer(milk_record)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update the details of a single milk record.
        """
        milk_record = Milk.objects.get(pk=pk)
        serializer = MilkSerializer(milk_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """
        Delete a single milk record.
        """
        milk_record = Milk.objects.get(pk=pk)
        milk_record.delete()
        return Response(status=204)

class LactationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LactationSerializer
    queryset = Lactation.objects.all()
    
class PregnancyViewSet(viewsets.ModelViewSet):
    queryset = Pregnancy.objects.all()
    serializer_class = PregnancySerializer


class MilkTodayView(APIView):
    def get(self, request, format=None):
        today = timezone.localdate()
        start_of_today = timezone.datetime.combine(today, timezone.datetime.min.time())
        end_of_today = timezone.datetime.combine(today, timezone.datetime.max.time())

        yesterday = today - timezone.timedelta(days=1)
        start_of_yesterday = timezone.datetime.combine(yesterday, timezone.datetime.min.time())
        end_of_yesterday = timezone.datetime.combine(yesterday, timezone.datetime.max.time())

        total_milk_today = Milk.objects.filter(milking_date__range=(start_of_today, end_of_today)).aggregate(Sum('amount_in_kgs'))['amount_in_kgs__sum'] or 0
        total_milk_yesterday = Milk.objects.filter(milking_date__range=(start_of_yesterday, end_of_yesterday)).aggregate(Sum('amount_in_kgs'))['amount_in_kgs__sum'] or 0

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
        total_alive_female_cows = Cow.objects.filter(availability_status='Alive', gender='Female').values('id').distinct().count()
        return Response({'total_alive_female_cows': total_alive_female_cows})

class TotalAliveMaleCowsView(APIView):
    def get(self, request, format=None):
        total_alive_male_cows = Cow.objects.filter(availability_status='Alive', gender='Male').values('id').distinct().count()
        return Response({'total_alive_male_cows': total_alive_male_cows})

class CowsMilkedTodayView(APIView):
    def get(self, request, format=None):
        today = timezone.localdate()
        start_of_day = timezone.datetime.combine(today, timezone.datetime.min.time())
        end_of_day = timezone.datetime.combine(today, timezone.datetime.max.time())
        milking_cows = Milk.objects.filter(milking_date__range=(start_of_day, end_of_day)).values('cow_id').distinct()
        milked_cows = milking_cows.count()

        return Response({
            'cows_milked_today': milked_cows,})

class MilkProductionWeeklyView(APIView):
    def get(self, request, format=None):
        today = timezone.localdate()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=7)

        # Get all milk records for the week
        milk_records = Milk.objects.filter(milking_date__range=(start_of_week, end_of_week)).order_by('milking_date')

        # Create a dictionary to store the milk records grouped by day
        milk_production_data = {}
        for record in milk_records:
            day = record.milking_date.strftime('%A')
            if day not in milk_production_data:
                milk_production_data[day] = {'day': day, 'total_milk': record.amount_in_kgs}
            else:
                milk_production_data[day]['total_milk'] += record.amount_in_kgs

        # Convert the dictionary into a list of dictionaries
        milk_production_data = [{'day': day, 'milk_records': [record]} for day, record in milk_production_data.items()]

        return Response(milk_production_data)

class PregnantCowsView(APIView):
    def get(self, request, format=None):
        pregnancies_count = Pregnancy.objects.filter(pregnancy_status='Confirmed', date_of_calving__isnull=True).count()
        return Response({'pregnancies_count':pregnancies_count})

class LactatingCowsView(APIView):
    def get(self, request, format=None):
        lactating_cows = Lactation.objects.filter(end_date__isnull=True).values_list('cow__name', flat=True)
        lactating_cows_count = lactating_cows.count()
        
        # Return the response
        return Response({'lactating_cows_count': lactating_cows_count, 'lactating_cows': lactating_cows})

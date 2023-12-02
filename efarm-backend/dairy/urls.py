from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'dairy'

router = routers.DefaultRouter()
router.register(r'cows', CowViewSet, basename='cows')
router.register(r'cow-breeds', CowBreedViewSet, basename='cow-breeds')
router.register(r'heat-records', HeatViewSet, basename='heat-records')
router.register(r'inseminator-records', InseminatorViewset, basename='inseminator-records')
router.register(r'insemination-records', InseminationViewset, basename='insemination-records')
router.register(r'milk-records', MilkViewSet, basename='milk-records')
router.register(r'lactation-records', LactationViewSet, basename='lactation-records')
router.register(r'pregnancy-records', PregnancyViewSet, basename='pregnancy-records')
# router.register(r'symptoms-records', SymptomsViewSet, basename='symptoms-records')
router.register(r'weight-records', WeightRecordViewSet, basename='weight-records')
router.register(r'culling-records', CullingRecordViewSet, basename='culling-records')
router.register(r'quarantine-records', QuarantineRecordViewSet, basename='quarantine-records')
router.register(r'barns', BarnViewSet, basename='barns')
router.register(r'cow-pens', CowPenViewSet, basename='cow-pens')
router.register(r'cow-in-pen-movements', CowInPenMovementViewSet, basename='cow-in-pen-movements')
router.register(r'cow-in-barn-movements', CowInBarnMovementViewSet, basename='cow-in-barn-movements')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/dashboard/daily-milk-production', MilkTodayView.as_view()),
    path('admin/dashboard/milked-cows', CowsMilkedTodayView.as_view()),
    path('admin/dashboard/total-alive-cows', TotalAliveCowsView.as_view()),
    path('admin/dashboard/total-alive-male-cows', TotalAliveMaleCowsView.as_view()),
    path('admin/dashboard/total-alive-female-cows', TotalAliveFemaleCowsView.as_view()),
    path('admin/dashboard/weekly-milk-chart-data', MilkProductionWeeklyView.as_view()),
    path('admin/dashboard/pregnant-cows', PregnantCowsView.as_view()),
    path('admin/dashboard/lactating-cows', LactatingCowsView.as_view()),
]

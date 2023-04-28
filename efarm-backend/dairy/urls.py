from django.urls import path, include
from rest_framework import routers
from .views import * 

app_name='dairy'


router = routers.DefaultRouter()
router.register(r'cows', CowViewSet)
router.register(r'milk', MilkViewSet)
router.register(r'lactations', LactationViewSet)
router.register(r'pregnancies', PregnancyViewSet)

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
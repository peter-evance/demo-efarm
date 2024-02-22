from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from users.views import *

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', CustomUserViewSet, basename='users')

urlpatterns = [
    path('login/', TokenCreateView.as_view(), name='login'),
    path('logout/', TokenDestroyView.as_view(), name='logout'),
    path('generate-username', GenerateUsernameSlugAPIView.as_view(), name='generate-username'),

    path('assign-farm-owner/', AssignFarmOwnerView.as_view(), name='assign-farm-owner'),
    path('assign-farm-manager/', AssignFarmManagerView.as_view(), name='assign-farm-manager'),
    path('assign-assistant-farm-manager/', AssignAssistantFarmManagerView.as_view(), name='assign-assistant-farm-manager'),
    path('assign-team-leader/', AssignTeamLeaderView.as_view(), name='assign-team-leader'),
    path('assign-farm-worker/', AssignFarmWorkerView.as_view(), name='assign-farm-worker'),

    path('dismiss-farm-manager/', DismissFarmManagerView.as_view(), name='dismiss-farm-manager'),
    path('dismiss-assistant-farm-manager/', DismissAssistantFarmManagerView.as_view(), name='dismiss-assistant-farm-manager'),
    path('dismiss-team-leader/', DismissTeamLeaderView.as_view(), name='dismiss-team-leader'),
    path('dismiss-farm-worker/', DismissFarmWorkerView.as_view(), name='dismiss-farm-worker'),

    path('', include(router.urls))
]

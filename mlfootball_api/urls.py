from django.urls import path
from .views import MatchList

app_name = 'mlfootball_api'

urlpatterns = [
    path('matchlist/', MatchList.as_view())
]
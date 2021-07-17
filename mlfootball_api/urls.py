from django.urls import path
from .views import MatchList, TeamList

app_name = 'mlfootball_api'

urlpatterns = [
    path('matches/<str:date>/', MatchList.as_view()),
    path('teams/<int:season>/<str:league_id>/', TeamList.as_view())
]
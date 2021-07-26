from django.urls import path
from .views import *

app_name = 'mlfootball_api'

urlpatterns = [
    path('matches/<str:date>/', MatchList.as_view()),
    path('match_detail/<int:match_id>/', MatchStats.as_view()),
    path('standings/<int:season>/<int:league_id>/',Standings.as_view()),
    path('teams/<int:season>/<int:league_id>/<str:team>/', Team.as_view())
]
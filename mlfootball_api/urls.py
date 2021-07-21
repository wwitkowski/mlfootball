from django.urls import path
from .views import MatchList, Standings

app_name = 'mlfootball_api'

urlpatterns = [
    path('matches/<str:date>/', MatchList.as_view()),
    path('standings/<int:season>/<str:league_id>/', Standings.as_view())
]
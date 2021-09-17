from django.urls import path, re_path   
from .views import *

app_name = 'mlfootball_api'

urlpatterns = [
    path('matches/<int:match_id>/', MatchStats.as_view()),
    path('matches/<str:date>/', MatchList.as_view()),
    re_path(r'^standings/$', Standings.as_view()),
    re_path(r'^teams/stats/total/$', TeamStatsTotal.as_view()),
    re_path(r'^teams/stats/weighted/$', TeamStatsWeight.as_view()),
    path('predictions/similar/', similar),
    path('predictions/neuralnet/', neuralnet_predict),
    path('lastupdate/', LastUpdated.as_view())
]
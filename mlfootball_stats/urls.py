from django.urls import path
from .views import home_view, match_stats_view

app_name = 'mlfootball_stats'

urlpatterns = [
    path('', home_view),
    path('<int:match_id>/', match_stats_view)
]
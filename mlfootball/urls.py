from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mlfootball_stats.urls', namespace='mlfootball_stats')),
    path('api/', include('mlfootball_api.urls', namespace='mlfootball_api'))
]

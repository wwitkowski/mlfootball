from django.shortcuts import render
from django.db.models import Avg, Count, Min, Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StatsSerializer, TeamSerializer
from .models import Stats


# Create your views here.
class MatchList(APIView):
    def get(self, request, date, format=None):
        queryset = Stats.objects.filter(date=date)
        serializer = StatsSerializer(queryset, many=True)
        return Response(serializer.data)


class TeamList(APIView):
    def get(self, request, season, league_id, format=None):
        quertyset = Stats.objects.filter(league_id=league_id, season=season) \
            .values('league','team1') \
            .annotate(
                num_matches=Count('team1'),
                points=Sum('pts1'),
                
            ).order_by('-points')
        serializer = TeamSerializer(quertyset, many=True)
        return Response(serializer.data)
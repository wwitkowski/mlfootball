import collections
from django.shortcuts import render
from django.db.models import Avg, Count, Min, Sum, F, Case, When, Value

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from .serializers import MatchSerializer, StatsStandingsSerializer, TeamStandingsSerializer
from .models import Match

from operator import itemgetter


# Create your views here.
class MatchList(APIView):
    def get(self, request, date, format=None):
        queryset = Match.objects.filter(date=date)
        serializer = MatchSerializer(queryset, many=True)
        return Response(serializer.data)


class Standings(APIView):
    def get(self, *args, **kwargs):
        result = list()
        teams_queryset = Match.objects.filter(league_id=self.kwargs['league_id'], season=self.kwargs['season']) \
            .values('team1') \
            .annotate(name=F('team1')).distinct()
        home_stats_queryset = Match.objects.filter(league_id=self.kwargs['league_id'], season=self.kwargs['season']) \
            .values('team1') \
            .annotate(
                played=Count('team1'),
                wins=Sum(Case(
                    When(ftr=Value('H'), then=1),
                    default=0
                )),
                draws=Sum(Case(
                    When(ftr=Value('D'), then=1),
                    default=0
                )),
                losses=Sum(Case(
                    When(ftr=Value('A'), then=1),
                    default=0
                )),   
                points=Sum('pts1'),
                scored=Sum('score1'),
                conceded=Sum('score2'),
                xpoints=Sum('xpts1'),
                xgscored=Sum('xg1'),
                xgconceded=Sum('xg2')
            )

        away_stats_queryset = Match.objects.filter(league_id=self.kwargs['league_id'], season=self.kwargs['season']) \
            .values('team2') \
            .annotate(
                played=Count('team2'),
                wins=Sum(Case(
                    When(ftr=Value('A'), then=1),
                    default=0
                )),
                draws=Sum(Case(
                    When(ftr=Value('D'), then=1),
                    default=0
                )),
                losses=Sum(Case(
                    When(ftr=Value('H'), then=1),
                    default=0
                )),   
                points=Sum('pts2'),
                scored=Sum('score2'),
                conceded=Sum('score1'),
                xpoints=Sum('xpts2'),
                xgscored=Sum('xg2'),
                xgconceded=Sum('xg1')
            )
        
        for team in teams_queryset:
            team_serializer = TeamStandingsSerializer(team)
            team_name = team['team1']
            hteam_stats = list(filter(lambda hteam: hteam['team1'] == team_name, list(home_stats_queryset)))[0]
            ateam_stats = list(filter(lambda ateam: ateam['team2'] == team_name, list(away_stats_queryset)))[0]
            home_stats_serializer = StatsStandingsSerializer(hteam_stats)
            away_stats_serializer = StatsStandingsSerializer(ateam_stats)
            total_stats_serializer = StatsStandingsSerializer({k: hteam_stats.get(k, 0) + ateam_stats.get(k, 0) for k in set(hteam_stats) & set(ateam_stats)})
            result.append({'team': team_serializer.data, 
                            'home': home_stats_serializer.data, 
                            'away': away_stats_serializer.data,
                            'total': total_stats_serializer.data
                            })

        result_sorted = sorted(result, key=lambda e: e['total']['points'], reverse=True)
        result_wrank = [dict(item, rank=i+1) for i, item in enumerate(result_sorted)]

        return Response(result_wrank)


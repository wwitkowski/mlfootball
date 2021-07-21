import collections
from django.shortcuts import render
from django.db.models import Avg, Count, Min, Sum, F, Case, When, Value

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from .serializers import MatchSerializer, StatsStandingsSerializer, TeamStandingsSerializer
from .models import Match

from itertools import product


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
            .annotate(name=F('team1'))
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
        
        # for team in teams_queryset:
        #     for hteam_stats in home_stats_queryset:
        #         for ateam_stats in away_stats_queryset:
        #             if team['team1'] == hteam_stats['team1'] == ateam_stats['team2']:
        #                 team_serializer = TeamStandingsSerializer(team)
        #                 home_stats_serializer = StatsStandingsSerializer(hteam_stats)
        #                 away_stats_serializer = StatsStandingsSerializer(ateam_stats)
        #                 total_stats_serializer = StatsStandingsSerializer({k: hteam_stats.get(k, 0) + ateam_stats.get(k, 0) for k in set(hteam_stats) & set(ateam_stats)})
        #                 result.append({'team': team_serializer.data, 
        #                                'home': home_stats_serializer.data, 
        #                                'away': away_stats_serializer.data,
        #                                'total': total_stats_serializer.data})

        product_stat_list = [product_stat for product_stat in product(teams_queryset, home_stats_queryset, away_stats_queryset) if product_stat[0]['name'] == product_stat[1]['team1'] == product_stat[2]['team2']]
        for product_stat in product_stat_list:
            #if product_stat[0]['name'] == product_stat[1]['team1'] == product_stat[2]['team2']:
                team_serializer = TeamStandingsSerializer(product_stat[0])
                home_stats_serializer = StatsStandingsSerializer(product_stat[1])
                away_stats_serializer = StatsStandingsSerializer(product_stat[2])
                total_stats_serializer = StatsStandingsSerializer({k: product_stat[1].get(k, 0) + product_stat[2].get(k, 0) for k in set(product_stat[1]) & set(product_stat[2])})
                result.append({'team': team_serializer.data, 
                                'home': home_stats_serializer.data, 
                                'away': away_stats_serializer.data,
                                'total': total_stats_serializer.data})


        return Response(result)


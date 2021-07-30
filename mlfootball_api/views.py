import collections
from django.shortcuts import render
from django.db.models import Q, Avg, Count, Min, Sum, F, Case, When, Value

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from .models import Match


# Create your views here.
class MatchList(APIView):
    def get(self, request, date, format=None):
        queryset = Match.objects.filter(date=date)
        serializer = MatchSerializer(queryset, many=True)
        return Response(serializer.data)


class MatchStats(APIView):
    def get(self, *args, **kwargs):
        match_queryset = Match.objects.filter(id=self.kwargs['match_id'])
        home_stats_queryset = match_queryset.annotate(
            rating=F('spi1'),
            importance=F('importance1'),
            xg=F('xg1'),
            nsxg=F('nsxg1'),
            shots=F('shots1'),
            shots_ot=F('shotsot1'),
            corners=F('corners1'),
            fouls=F('fouls1'),
            yellow=F('yellow1'),
            red=F('red1'),
            xpts=F('xpts1'),
            xg_shot=F('xgshot1'),
        )
        away_stats_queryset = match_queryset.annotate(
            rating=F('spi2'),
            importance=F('importance2'),
            xg=F('xg2'),
            nsxg=F('nsxg2'),
            shots=F('shots2'),
            shots_ot=F('shotsot2'),
            corners=F('corners2'),
            fouls=F('fouls2'),
            yellow=F('yellow2'),
            red=F('red2'),
            xpts=F('xpts2'),
            xg_shot=F('xgshot2'),
        )

        match_serializer = MatchSerializer(match_queryset[0])
        home_stats_serializer = MatchStatsSeriazlier(home_stats_queryset[0])
        away_stats_serializer = MatchStatsSeriazlier(away_stats_queryset[0])      
        result = { 
            'match': match_serializer.data,
            'home': home_stats_serializer.data,
            'away': away_stats_serializer.data
        }

        return Response(result)


class Standings(APIView):
    def get(self, *args, **kwargs):
        result = list()
        league_id = self.request.query_params.get('league')
        season = self.request.query_params.get('season')

        teams_queryset = Match.objects.filter(league_id=league_id, season=season) \
            .values('team1') \
            .annotate(name=F('team1')).distinct()
        home_stats_queryset = Match.objects.filter(league_id=league_id, season=season) \
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
        away_stats_queryset = Match.objects.filter(league_id=league_id, season=season) \
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
            team_serializer = TeamSerializer(team)
            team_name = team['team1']
            hteam_stats = list(filter(lambda hteam: hteam['team1'] == team_name, list(home_stats_queryset)))[0]
            ateam_stats = list(filter(lambda ateam: ateam['team2'] == team_name, list(away_stats_queryset)))[0]
            home_stats_serializer = StatsStandingsSerializer(hteam_stats)
            away_stats_serializer = StatsStandingsSerializer(ateam_stats)
            total_stats_serializer = StatsStandingsSerializer({k: hteam_stats.get(k, 0) + ateam_stats.get(k, 0) for k in set(hteam_stats) & set(ateam_stats)})
            result.append({
                'team': team_serializer.data, 
                'home': home_stats_serializer.data, 
                'away': away_stats_serializer.data,
                'total': total_stats_serializer.data
            })
        result_sorted = sorted(result, key=lambda e: e['total']['points'], reverse=True)
        result_wrank = [dict(item, rank=i+1) for i, item in enumerate(result_sorted)]

        return Response(result_wrank)


class TeamStatsTotal(APIView):
    def get(self, *args, **kwargs):
        league_id = self.request.query_params.get('league')
        season = self.request.query_params.get('season')
        team_name = self.request.query_params.get('team')

        team_queryset = Match.objects.filter(league_id=league_id, season=season, team1=team_name) \
        .values('team1') \
        .annotate(name=F('team1')).distinct()
        home_stats_queryset = Match.objects.filter(league_id=league_id, season=season, team1=team_name) \
            .values('team1') \
            .annotate(
                played=Count('team1'),
                points=Sum('pts1'),
                scored=Sum('score1'),
                conceded=Sum('score2'),
                xpoints=Sum('xpts1'),
                xgscored=Sum('xg1'),
                xgconceded=Sum('xg2'),
                nsxgscored=Sum('nsxg1'),
                nsxgconceded=Sum('nsxg2'),
                shots_scored=Sum('shots1'),
                shotsot_scored=Sum('shotsot1'),
                corners_scored=Sum('corners1'),
                fouls_scored=Sum('fouls1'),
                yellow_scored=Sum('yellow1'),
                red_scored=Sum('red1'),
                #xgshot_scored=Sum('xg1')/Sum('shots1'),
                #convrate_scored=Sum('score1')/Sum('shots1'),
                shots_conceded=Sum('shots2'),
                shotsot_conceded=Sum('shotsot2'),
                corners_conceded=Sum('corners2'),
                fouls_conceded=Sum('fouls2'),
                yellow_conceded=Sum('yellow2'),
                red_conceded=Sum('red2'),
                #xgshot_conceded=Sum('xg2')/Sum('shots2'),
                #convrate_conceded=Sum('score2')/Sum('shots2'),
            )
        away_stats_queryset = Match.objects.filter(league_id=league_id, season=season, team1=team_name) \
            .values('team2') \
            .annotate(
                played=Count('team2'),
                points=Sum('pts2'),
                scored=Sum('score2'),
                conceded=Sum('score1'),
                xpoints=Sum('xpts2'),
                xgscored=Sum('xg2'),
                xgconceded=Sum('xg1'),
                nsxgscored=Sum('nsxg2'),
                nsxgconceded=Sum('nsxg1'),
                shots_scored=Sum('shots2'),
                shotsot_scored=Sum('shotsot2'),
                corners_scored=Sum('corners2'),
                fouls_scored=Sum('fouls2'),
                yellow_scored=Sum('yellow2'),
                red_scored=Sum('red2'),
                # xgshot_scored=Sum('xg2')/Sum('shots2'),
                # convrate_scored=Sum('score2')/Sum('shots2'),
                shots_conceded=Sum('shots1'),
                shotsot_conceded=Sum('shotsot1'),
                corners_conceded=Sum('corners1'),
                fouls_conceded=Sum('fouls1'),
                yellow_conceded=Sum('yellow1'),
                red_conceded=Sum('red1'),
                # xgshot_conceded=Sum('xg1')/Sum('shots1'),
                # convrate_conceded=Sum('score1')/Sum('shots1'),
            )
        team_serializer = TeamSerializer(team_queryset[0])
        home_stats_serializer = StatsTotalSerializer(home_stats_queryset[0])
        away_stats_serializer = StatsTotalSerializer(away_stats_queryset[0])
        total_stats_serializer = StatsTotalSerializer(
            {k: home_stats_queryset[0].get(k, 0) + away_stats_queryset[0].get(k, 0) for k in set(home_stats_queryset[0]) & set(away_stats_queryset[0])}
        )
        result = {
            'team': team_serializer.data,
            'home': home_stats_serializer.data,
            'away': away_stats_serializer.data,
            'total': total_stats_serializer.data
        }

        return Response(result)


class TeamStatsWeight(APIView):
    def get(self, *args, **kwargs):
        league_id = self.request.query_params.get('league')
        team_name = self.request.query_params.get('team')
        count = int(self.request.query_params.get('count'))

        team_queryset = Match.objects.filter(league_id=league_id, team1=team_name) \
        .values('team1') \
        .annotate(name=F('team1')).distinct()
        query_home = ''' 
            SELECT 1 id, team1,
            Sum(pts1*weight)/Sum(weight) AS points,
            Sum(score1*weight)/Sum(weight) AS scored,
            Sum(score2*weight)/Sum(weight) AS conceded,
            Sum(xpts1*weight)/Sum(weight) AS xpoints,
            Sum(xg1*weight)/Sum(weight) AS xgscored,
            Sum(xg2*weight)/Sum(weight) AS xgconceded,
            Sum(nsxg1*weight)/Sum(weight) AS nsxgscored,
            Sum(nsxg2*weight)/Sum(weight) AS nsxgconceded,
            Sum(shots1*weight)/Sum(weight) AS shots_scored,
            Sum(shotsot1*weight)/Sum(weight) AS shotsot_scored,
            Sum(corners1*weight)/Sum(weight) AS corners_scored,
            Sum(fouls1*weight)/Sum(weight) AS fouls_scored,
            Sum(yellow1*weight)/Sum(weight) AS yellow_scored,
            Sum(red1*weight)/Sum(weight) AS red_scored,
            Sum(shots2*weight)/Sum(weight) AS shots_conceded,
            Sum(shotsot2*weight)/Sum(weight) AS shotsot_conceded,
            Sum(corners2*weight)/Sum(weight) AS corners_conceded,
            Sum(fouls2*weight)/Sum(weight) AS fouls_conceded,
            Sum(yellow2*weight)/Sum(weight) AS yellow_conceded,
            Sum(red2*weight)/Sum(weight) AS red_conceded
            from matches m
            INNER JOIN (
                SELECT id from matches
                where league_id = %s
                and team1 = %s
                ORDER BY id DESC
                LIMIT %s) last ON m.id = last.id
            GROUP BY team1
            '''
        home_stats_queryset = Match.objects.raw(query_home, params=[league_id, team_name, count])
        query_away = ''' 
            SELECT 1 id, team2,
            Sum(pts2*weight)/Sum(weight) AS points,
            Sum(score2*weight)/Sum(weight) AS scored,
            Sum(score1*weight)/Sum(weight) AS conceded,
            Sum(xpts2*weight)/Sum(weight) AS xpoints,
            Sum(xg2*weight)/Sum(weight) AS xgscored,
            Sum(xg1*weight)/Sum(weight) AS xgconceded,
            Sum(nsxg2*weight)/Sum(weight) AS nsxgscored,
            Sum(nsxg1*weight)/Sum(weight) AS nsxgconceded,
            Sum(shots2*weight)/Sum(weight) AS shots_scored,
            Sum(shotsot2*weight)/Sum(weight) AS shotsot_scored,
            Sum(corners2*weight)/Sum(weight) AS corners_scored,
            Sum(fouls2*weight)/Sum(weight) AS fouls_scored,
            Sum(yellow2*weight)/Sum(weight) AS yellow_scored,
            Sum(red2*weight)/Sum(weight) AS red_scored,
            Sum(shots1*weight)/Sum(weight) AS shots_conceded,
            Sum(shotsot1*weight)/Sum(weight) AS shotsot_conceded,
            Sum(corners1*weight)/Sum(weight) AS corners_conceded,
            Sum(fouls1*weight)/Sum(weight) AS fouls_conceded,
            Sum(yellow1*weight)/Sum(weight) AS yellow_conceded,
            Sum(red1*weight)/Sum(weight) AS red_conceded
            from matches m
            INNER JOIN (
                SELECT id from matches
                where league_id = %s
                and team2 = %s
                ORDER BY id DESC
                LIMIT %s) last ON m.id = last.id
            GROUP BY team2
            '''
        away_stats_queryset = Match.objects.raw(query_away, params=[league_id, team_name, count])

        query_total = '''
        SELECT 1 id, team1,
        Sum(pts1*weight)/Sum(weight) AS points,
        Sum(score1*weight)/Sum(weight) AS scored,
        Sum(score2*weight)/Sum(weight) AS conceded,
        Sum(xpts1*weight)/Sum(weight) AS xpoints,
        Sum(xg1*weight)/Sum(weight) AS xgscored,
        Sum(xg2*weight)/Sum(weight) AS xgconceded,
        Sum(nsxg1*weight)/Sum(weight) AS nsxgscored,
        Sum(nsxg2*weight)/Sum(weight) AS nsxgconceded,
        Sum(shots1*weight)/Sum(weight) AS shots_scored,
        Sum(shotsot1*weight)/Sum(weight) AS shotsot_scored,
        Sum(corners1*weight)/Sum(weight) AS corners_scored,
        Sum(fouls1*weight)/Sum(weight) AS fouls_scored,
        Sum(yellow1*weight)/Sum(weight) AS yellow_scored,
        Sum(red1*weight)/Sum(weight) AS red_scored,
        Sum(shots2*weight)/Sum(weight) AS shots_conceded,
        Sum(shotsot2*weight)/Sum(weight) AS shotsot_conceded,
        Sum(corners2*weight)/Sum(weight) AS corners_conceded,
        Sum(fouls2*weight)/Sum(weight) AS fouls_conceded,
        Sum(yellow2*weight)/Sum(weight) AS yellow_conceded,
        Sum(red2*weight)/Sum(weight) AS red_conceded	
        FROM (
            (SELECT id,
            weight,
            team1,
            pts1,
            score1,
            score2,
            xpts1,
            xg1,
            xg2,
            nsxg1,
            nsxg2,
            shots1,
            shotsot1,
            corners1,
            fouls1,
            yellow1,
            red1,
            shots2,
            shotsot2,
            corners2,
            fouls2,
            yellow2,
            red2
            from matches
            where league_id = %s
            and team1 = %s)
            UNION
            (SELECT id,
            weight,
            team2 as team1, 
            pts2 as pts1,
            score2 as score1,
            score1 as score2,
            xpts2 as xpts1,
            xg2 as xg1,
            xg1 as xg2,
            nsxg2 as nsxg1,
            nsxg1 as nsxg2,
            shots2 as shots1,
            shotsot2 as shotsot1,
            corners2 as corners1,
            fouls2 as fouls1,
            yellow2 as yellow1,
            red2 as red1,
            shots1 as shots2,
            shotsot1 as shotsot2,
            corners1 as corners2,
            fouls1 as fouls2,
            yellow1 as yellow2,
            red1 as red2
            from matches
            where league_id = %s
            and team2 = %s
            )
            ORDER BY ID DESC
            LIMIT %s) m
        GROUP BY team1
        '''
        total_stats_queryset = Match.objects.raw(query_total, params=[league_id, team_name, league_id, team_name, count])
        team_serializer = TeamSerializer(team_queryset[0])
        home_stats_serializer = StatsWeightedSerializer(home_stats_queryset[0])
        away_stats_serializer = StatsWeightedSerializer(away_stats_queryset[0])
        total_stats_serializer = StatsWeightedSerializer(total_stats_queryset[0])

        result = {
            'team': team_serializer.data,
            'home': home_stats_serializer.data,
            'away': away_stats_serializer.data,
            'total': total_stats_serializer.data
        }

        return Response(result)



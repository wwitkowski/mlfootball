from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id',
            'date',
            'league',
            'team1',
            'team2',
            'score1',
            'score2'
        )


class TeamStandingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Match
        fields = (
            'name',
        )


class StatsStandingsSerializer(serializers.ModelSerializer):
    played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    points = serializers.IntegerField()
    scored = serializers.IntegerField()
    conceded = serializers.IntegerField()
    xpoints = serializers.FloatField()
    xgscored = serializers.FloatField()
    xgconceded = serializers.FloatField()


    class Meta:
        model = Match
        fields = (
            'played',
            'wins',
            'draws',
            'losses',
            'points',
            'scored',
            'conceded',
            'xpoints',
            'xgscored',
            'xgconceded',
        )

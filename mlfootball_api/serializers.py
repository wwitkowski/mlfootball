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
            'score2',
            'ftr'
        )


class MatchStatsSeriazlier(serializers.ModelSerializer):
    rating = serializers.FloatField()
    importance = serializers.FloatField()
    xg = serializers.FloatField()
    nsxg = serializers.FloatField()
    shots = serializers.FloatField()
    shots_ot = serializers.FloatField()
    corners = serializers.FloatField()
    fouls = serializers.FloatField()
    yellow = serializers.FloatField()
    red = serializers.FloatField()
    xpts = serializers.FloatField()
    xg_shot = serializers.FloatField()

    class Meta:
        model = Match
        fields = (
            'rating',
            'importance',
            'xg',
            'nsxg',
            'shots',
            'shots_ot',
            'corners',
            'fouls',
            'yellow',
            'red',
            'xpts',
            'xg_shot'
        )


class TeamSerializer(serializers.ModelSerializer):
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


class StatsSerializer(serializers.ModelSerializer):
    played = serializers.IntegerField()
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
            'points',
            'scored',
            'conceded',
            'xpoints',
            'xgscored',
            'xgconceded',
        )
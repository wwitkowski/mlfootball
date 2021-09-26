from rest_framework import serializers
from .models import Match


class BaseMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


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


class DateSerializer(serializers.ModelSerializer):
    last_updated = serializers.DateField()

    class Meta:
        model = Match
        fields = (
            'last_updated',
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


class StatsTotalSerializer(serializers.ModelSerializer):
    played = serializers.IntegerField()
    points = serializers.IntegerField()
    scored = serializers.IntegerField()
    conceded = serializers.IntegerField()
    xpoints = serializers.FloatField()
    xgscored = serializers.FloatField()
    xgconceded = serializers.FloatField()
    nsxgscored = serializers.FloatField()
    nsxgconceded = serializers.FloatField()
    shots_scored = serializers.IntegerField()
    shotsot_scored = serializers.IntegerField()
    corners_scored = serializers.IntegerField()
    fouls_scored = serializers.IntegerField()
    yellow_scored = serializers.IntegerField()
    red_scored = serializers.IntegerField()
    # xgshot_scored = serializers.FloatField()
    # convrate_scored = serializers.FloatField()
    shots_conceded = serializers.IntegerField()
    shotsot_conceded = serializers.IntegerField()
    corners_conceded = serializers.IntegerField()
    fouls_conceded = serializers.IntegerField()
    yellow_conceded = serializers.IntegerField()
    red_conceded = serializers.IntegerField()
    # xgshot_conceded = serializers.FloatField()
    # convrate_conceded = serializers.FloatField()

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
            'nsxgscored',
            'nsxgconceded',
            'shots_scored',
            'shotsot_scored',
            'corners_scored',
            'fouls_scored',
            'yellow_scored',
            'red_scored',
            # 'xgshot_scored',
            # 'convrate_scored',
            'shots_conceded',
            'shotsot_conceded',
            'corners_conceded',
            'fouls_conceded',
            'yellow_conceded',
            'red_conceded',
            # 'xgshot_conceded',
            # 'convrate_conceded'
        )


class StatsWeightedSerializer(serializers.ModelSerializer):
    points = serializers.FloatField()
    scored = serializers.FloatField()
    conceded = serializers.FloatField()
    xpoints = serializers.FloatField()
    xgscored = serializers.FloatField()
    xgconceded = serializers.FloatField()
    nsxgscored = serializers.FloatField()
    nsxgconceded = serializers.FloatField()
    shots_scored = serializers.FloatField()
    shotsot_scored = serializers.FloatField()
    corners_scored = serializers.FloatField()
    fouls_scored = serializers.FloatField()
    yellow_scored = serializers.FloatField()
    red_scored = serializers.FloatField()
    # xgshot_scored = serializers.FloatField()
    # convrate_scored = serializers.FloatField()
    shots_conceded = serializers.FloatField()
    shotsot_conceded = serializers.FloatField()
    corners_conceded = serializers.FloatField()
    fouls_conceded = serializers.FloatField()
    yellow_conceded = serializers.FloatField()
    red_conceded = serializers.FloatField()
    # xgshot_conceded = serializers.FloatField()
    # convrate_conceded = serializers.FloatField()

    class Meta:
        model = Match
        fields = (
            'points',
            'scored',
            'conceded',
            'xpoints',
            'xgscored',
            'xgconceded',
            'nsxgscored',
            'nsxgconceded',
            'shots_scored',
            'shotsot_scored',
            'corners_scored',
            'fouls_scored',
            'yellow_scored',
            'red_scored',
            # 'xgshot_scored',
            # 'convrate_scored',
            'shots_conceded',
            'shotsot_conceded',
            'corners_conceded',
            'fouls_conceded',
            'yellow_conceded',
            'red_conceded',
            # 'xgshot_conceded',
            # 'convrate_conceded'
        )


class SimilarRatingSerializer(serializers.ModelSerializer):
    win = serializers.FloatField()
    draw = serializers.FloatField()
    loss = serializers.FloatField()
    avg_score1 = serializers.FloatField()
    avg_score2 = serializers.FloatField()

    class Meta:
        model = Match
        fields = (
            'win',
            'draw',
            'loss',
            'avg_score1',
            'avg_score2'
        )
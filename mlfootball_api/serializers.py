from rest_framework import serializers
from .models import Stats

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = (
            'id',
            'date',
            'league',
            'team1',
            'team2',
            'score1',
            'score2'
        )


class TeamSerializer(serializers.ModelSerializer):
    num_matches = serializers.IntegerField()
    points = serializers.IntegerField()
    ''' 
    scored = serializers.IntegerField()
    conceded = serializers.IntegerField()
    x_points = serializers.FloatField()
    xg_scored = serializers.FloatField()
    xg_conceded = serializers.FloatField()
    '''

    class Meta:
        model = Stats
        fields = (
            'league',
            'team1',
            'num_matches',
            'points',
            # 'scored',
            # 'conceded',
            # 'x_points',
            # 'xg_scored',
            # 'xg_conceded'
        )

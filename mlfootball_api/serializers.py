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
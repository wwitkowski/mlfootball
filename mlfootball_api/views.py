from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StatsSerializer
from .models import Stats


# Create your views here.
class MatchList(APIView):
    def get(self, request, date, format=None):
        queryset = Stats.objects.filter(date=date)
        serializer = StatsSerializer(queryset, many=True)
        return Response(serializer.data)
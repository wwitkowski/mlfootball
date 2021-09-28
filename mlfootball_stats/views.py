from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from itertools import groupby

import requests

# Create your views here.
def home_view(request):
    now = datetime.now().strftime('%Y-%m-%d')
    r = requests.get(f'http://127.0.0.1:8000/api/matches/{now}/')
    matches = r.json()
    
    def key_func(k):
        return k['league']
    matches = sorted(matches, key=key_func)
    context = {
        'match_list': [(key, list(value)) for key, value in groupby(matches, key_func)]
    }
    
    return render(request, 'mlfootball_stats/home.html', context)


def match_stats_view(request, match_id):
    context = {
        'match_id': match_id
    }
    
    return render(request, 'mlfootball_stats/stats_dashboard.html', context)




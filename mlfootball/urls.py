from django.urls import path
from django.views.generic import TemplateView

app_name = 'mlfootball'

urlpatterns = [
    path('', TemplateView.as_view(template_name="mlfootball/index.html"))
]
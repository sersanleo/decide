from django.urls import path
from .views import VisualizerView, get_list_votings

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('', get_list_votings),
]

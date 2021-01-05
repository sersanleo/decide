from django.urls import path
from .views import VisualizerView, get_global_view

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('global', get_global_view),
]
from django.urls import path
from .views import BoothView, check_census


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('check_user_vote/', check_census)
]

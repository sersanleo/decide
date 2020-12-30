from django.urls import path
from .views import BoothView, chage_style


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('reload/', chage_style, name = 'change_style'),
]

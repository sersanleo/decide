from django.urls import path
from .views import BoothView, style_change


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('9cff8fe0-b7e3-48cb-970f-13ae47f89426/', style_change, name = 'deuteranopia'),
]

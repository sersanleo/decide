from django.urls import path
from booth import views as booth_views


urlpatterns = [
    path('',booth_views.InicioView.as_view(), name="inicio"),
    path('login/', booth_views.LoginView.as_view(), name="login"),
    path('dashboard/', booth_views.DashboardView.as_view(), name="dashboard"),
    path('<int:voting_id>/', booth_views.BoothView.as_view(), name="votacion"),
]

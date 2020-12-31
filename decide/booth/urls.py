from django.urls import path
from booth import views as booth_views

urlpatterns = [
    path('', booth_views.LoginView.as_view(), name="login"),
    path('logout/', booth_views.LogoutView.as_view(), name="logout"),
    path('dashboard/', booth_views.dashboard_view, name="dashboard"),
    path('<int:voting_id>/', booth_views.BoothView.as_view, name="votacion")
]

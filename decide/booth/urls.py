from django.urls import path
from booth import views as booth_views


urlpatterns = [
    path('', booth_views.LoginView.as_view(), name="login"),
    path('dashboard/', booth_views.dashboardView, name="dashboard"),
    path('<int:voting_id>/<int:user_id>/', booth_views.BoothView.as_view(), name="votacion"),
]

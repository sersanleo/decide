from django.urls import path
from .views import IndexView


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
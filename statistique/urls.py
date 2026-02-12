from django.urls import path
from . import views

urlpatterns = [
    path('api/global/', views.api_stats_globales, name='api_stats_globales'),
    path('dashboard/<int:etudiant_id>/', views.dashboard_etudiant, name='dashboard_etudiant'),
]
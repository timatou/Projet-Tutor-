from django.urls import path
from . import views
urlpatterns = [
    # Cette URL renvoie le HTML (statistique.html)
    path('', views.page_statistiques, name='liste_statistiques'),
    
    # Cette URL renvoie le JSON (les chiffres)
    path('api/globales/', views.api_stats_globales, name='api_statistique_globales'),
    # urls.py
    path('api/etudiant/<int:etudiant_id>/', views.dashboard_etudiant, name='api_etudiant_detail'),
]
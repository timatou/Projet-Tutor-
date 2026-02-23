from django.urls import path
from . import views
urlpatterns = [
    # Cette URL renvoie le HTML (statistique.html)
    path('', views.page_statistiques, name='liste_statistiques'),
    
    # Cette URL renvoie le JSON (les chiffres)
    path('api/globales/', views.api_stats_globales,  name='api_stats_globales'),
        path('api/groupes/', views.api_groupes, name='api_groupes'),
        path('api/etudiants/groupe/', views.api_etudiants_par_groupe, name='api_etudiants_par_groupe'),
        path('api/etudiants/', views.api_etudiants_par_groupe, name='api_etudiants_par_groupe'),
    # urls.py
    path('api/etudiant/<int:etudiant_id>/', views.dashboard_etudiant, name='api_etudiant_detail'),
]
from django.urls import path
from . import views

urlpatterns = [
    # Page HTML principale
    path('', views.page_statistiques, name='liste_statistiques'),

    # APIs statistiques globales
    path('api/globales/', views.api_stats_globales, name='api_stats_globales'),

    # APIs groupes
    path('api/groupes/', views.api_groupes, name='api_groupes'),

    # APIs étudiants par groupe
    path('api/etudiants/groupe/', views.api_etudiants_par_groupe, name='api_etudiants_par_groupe'),

    # Détail d’un étudiant

]
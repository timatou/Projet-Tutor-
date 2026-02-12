from django.urls import path
from . import views

urlpatterns = [
    # 1. La page principale (l'interface HTML)
    path('liste/', views.liste_etudiants, name='liste_etudiants'),
    
    # 2. La route pour récupérer les données (utilisée par fetch('/api/data/'))
    path('api/data/', views.api_etudiants_data, name='api_data'),
    
    # 3. La route pour ajouter un étudiant (utilisée par le formulaire)
    path('api/ajouter/', views.api_ajouter_etudiant, name='api_ajouter'),
    
    # 4. La route pour supprimer (le <str:matricule> permet de savoir qui effacer)
    path('api/supprimer/<str:matricule>/', views.api_supprimer_etudiant, name='api_supprimer'),

    path('api/groupes/', views.api_groupes_list, name='api_groupes'),
    
    path('api/promotions/', views.api_promotions_list),
]
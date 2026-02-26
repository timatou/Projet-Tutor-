from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Route pour la liste des enseignants
    path('enseignants/', views.liste_enseignants, name='liste_enseignants'),
    
    # Routes pour le login/logout
    path('login/', auth_views.LoginView.as_view(template_name='utilisateurs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Redirection après login
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('enseignants/ajouter/', views.ajouter_enseignant, name='ajouter_enseignant'),
    path('enseignants/editer/<int:pk>/', views.editer_enseignant, name='editer_enseignant'),

    path('tableau-de-bord/', views.dashboard_redirect, name='dashboard'), # Ta vue de redirection
    path('mon-espace/', views.espace_enseignant, name='espace_enseignant'), # <--- AJOUTE CETTE LIGNE
    path('saisir-notes/<int:module_id>/', views.saisir_notes_module, name='saisir_notes_module'), # Route pour la saisie des notes
    path('faire-appel/<int:module_id>/', views.faire_appel_module, name='faire_appel_module'), # Route pour faire l'appel
]
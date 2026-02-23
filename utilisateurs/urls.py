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
]
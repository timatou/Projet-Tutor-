from django.urls import path
from . import views

urlpatterns = [
    # C'est cette ligne qui permet d'accéder à la page via /cours/liste/
    path('liste/', views.liste_modules, name='liste_modules'),
    
    # Routes pour l'API (utilisées par ton JavaScript)
    path('api/data/', views.api_modules_data, name='api_modules_data'),
    path('api/ajouter/', views.api_ajouter_module, name='api_ajouter_module'),
    path('api/supprimer/<int:module_id>/', views.api_supprimer_module, name='api_supprimer_module'),
    path('editer/<int:module_id>/', views.editer_module, name='editer_module'),
]
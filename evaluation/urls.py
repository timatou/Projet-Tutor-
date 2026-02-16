from django.urls import path
from . import views

urlpatterns = [
    
    path('note/ajouter/', views.ajouter_note, name='ajouter_note'),
    #path('absence/saisir/', views.saisir_absence, name='saisir_absence'),
    path('api/note/ajouter/', views.api_ajouter_note, name='api_ajouter_note'),
    #path('api/absence/ajouter/', views.api_ajouter_absence, name='api_ajouter_absence'),

    path("api/notes/", views.api_notes),
    path("api/ajouter-note/", views.api_ajouter_note),
    path('notes/', views.notes_view, name='liste_notes'),
    path('api/supprimer-note/<int:id>/', views.api_supprimer_note, name='api_supprimer_note'),
]
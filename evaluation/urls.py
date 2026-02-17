from django.urls import path
from . import views

urlpatterns = [
    
    path('note/ajouter/', views.ajouter_note, name='ajouter_note'),
    path('api/note/ajouter/', views.api_ajouter_note, name='api_ajouter_note'),
    path('api/absence/ajouter/', views.api_ajouter_absence, name='api_ajouter_absence'),

    path("api/notes/", views.api_notes),
    path("api/ajouter-note/", views.api_ajouter_note),
    path('notes/', views.notes_view, name='liste_notes'),
    path('api/supprimer-note/<int:id>/', views.api_supprimer_note, name='api_supprimer_note'),


     #path('absence/saisir/', views.saisir_absence, name='saisir_absence'),
     path('absences/ajouter/', views.saisir_absence, name='ajouter_absence'),
    path('api/absences/ajouter/', views.api_ajouter_absence, name='api_ajouter_absence'),

    path("api/absences/", views.api_absences),
    path("api/ajouter-absence/", views.api_ajouter_absence),
    path('absences/', views.absence_view, name='liste_absences'),
    path('api/supprimer-note/<int:id>/', views.api_supprimer_note, name='api_supprimer_note'),
    path('api/supprimer-absence/<int:id>/', views.api_supprimer_absence, name='api_supprimer_absence'),
]



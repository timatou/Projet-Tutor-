from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # ======== NOTES ===========
    # ==========================
    path('notes/', views.notes_view, name='liste_notes'),

    path('api/notes/', views.api_notes, name='api_notes'),
    path('api/notes/ajouter/', views.api_ajouter_note, name='api_ajouter_note'),
    
    path('api/notes/supprimer/<int:id>/', views.api_supprimer_note, name='api_supprimer_note'),

    # ==========================
    # ====== EPREUVES ==========
    # ==========================
    path('api/epreuves/', views.api_epreuves, name='api_epreuves'),

    # ==========================
    # ====== ABSENCES ==========
    # ==========================
    path('absences/', views.absence_view, name='liste_absences'),

    path('api/absences/', views.api_absences, name='api_absences'),
    path('api/ajouter-absence/', views.api_ajouter_absence, name='api_ajouter_absence'),
    
    path('api/absences/supprimer/<int:id>/', views.api_supprimer_absence, name='api_supprimer_absence'),
    path('api/absences/valider/<int:absence_id>/', views.api_valider_absence, name='api_valider_absence'),
    path('api/justifier-absence/<int:absence_id>/',views.api_valider_absence,name='api_justifier_absence'
),
]
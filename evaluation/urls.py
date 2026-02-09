from django.urls import path
from . import views

urlpatterns = [
    path('note/ajouter/', views.ajouter_note, name='ajouter_note'),
    path('absence/saisir/', views.saisir_absence, name='saisir_absence'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('liste/', views.liste_etudiants, name='liste_etudiants'),
]
from django.shortcuts import render
from .models import Etudiant, Promotion

def liste_etudiants(request):
    # Récupération de tous les étudiants avec optimisation des requêtes
    etudiants = Etudiant.objects.select_related('promotion', 'groupe').all()
    
    # On prépare une liste enrichie avec les indicateurs calculés au backend
    data_etudiants = []
    for etu in etudiants:
        data_etudiants.append({
            'instance': etu,
            'moyenne': etu.moyenne_generale(), # Indicateur de performance 
            'statut': etu.status_performance(), # Code couleur 
        })
    
    return render(request, 'etudiants/liste.html', {'etudiants_data': data_etudiants})
from django.http import JsonResponse
from cours.models import Module
from .models import Statistique

def api_stats_globales(request):
    """
    Retourne les statistiques de tous les modules au format JSON 
    pour alimenter les graphiques (barres/camembert).
    """
    modules = Module.objects.all()
    
    labels = []
    moyennes = []
    taux_reussite = []

    for module in modules:
        labels.append(module.libelle)
        # On utilise ta classe Statistique pour les calculs 
        moyennes.append(Statistique.moyenne_par_module(module))
        taux_reussite.append(module.taux_reussite())

    data = {
        'labels': labels,
        'moyennes': moyennes,
        'taux_reussite': taux_reussite,
    }
    
    return JsonResponse(data)
def dashboard_etudiant(request, etudiant_id):
    pass
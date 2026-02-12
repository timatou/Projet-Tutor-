import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Module

# Affiche la page HTML
def liste_modules(request):
    return render(request, 'cours/modules.html')

# Envoie les données au JavaScript
def api_modules_data(request):
    # On récupère les modules et leurs professeurs associés
    modules = Module.objects.prefetch_related('professeurs').all()
    liste_data = []
    
    for m in modules:
        # Correction ici : str(p) va utiliser ce que tu as défini dans def __str__(self) 
        # du modèle Professeur au lieu de chercher un champ 'nom' qui n'existe pas.
        profs_noms = ", ".join([str(p) for p in m.professeurs.all()])
        
        liste_data.append({
            'id': m.id,
            'code': m.code,
            'libelle': m.libelle,
            'coefficient': m.coefficient,
            'semestre': m.semestre,
            'professeurs': profs_noms if profs_noms else "Non assigné",
            'moyenne': m.calculer_moyenne(),
            'taux': m.taux_reussite(),
        })
    
    return JsonResponse({'modules': liste_data})
# Ajoute un module en base
@csrf_exempt
def api_ajouter_module(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            Module.objects.create(
                code=data.get('code'),
                libelle=data.get('libelle'),
                coefficient=data.get('coefficient'),
                semestre=data.get('semestre')
            )
            return JsonResponse({"message": "Succès"}, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"message": "Méthode non autorisée"}, status=405)

# Supprime un module
@csrf_exempt
def api_supprimer_module(request, module_id):
    if request.method == "DELETE":
        try:
            m = Module.objects.get(id=module_id)
            m.delete()
            return JsonResponse({"message": "Supprimé"})
        except Module.DoesNotExist:
            return JsonResponse({"message": "Non trouvé"}, status=404)
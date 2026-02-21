import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Etudiant, Promotion, Groupe

# 1. Vue pour afficher la page HTML
def liste_etudiants(request):
    return render(request, 'etudiants/etudiants.html')

# 2. Vue pour charger les données dans le tableau (lecture)
def api_etudiants_data(request):
    etudiants = Etudiant.objects.select_related('promotion', 'groupe').all()
    liste_data = []
    for etu in etudiants:
        liste_data.append({
            'matricule': etu.matricule,
            'nom': etu.nom,
            'prenom': etu.prenom,
            'email': etu.email,
            'promotion': etu.promotion.nom if etu.promotion else "N/A",
            'groupe': etu.groupe.nom if etu.groupe else "Aucun",
            'moyenne': etu.moyenne_generale() if hasattr(etu, 'moyenne_generale') else 0,   
            'statut': etu.status_performance() if hasattr(etu, 'status_performance') else "Inconnu", 
        })
    return JsonResponse({'etudiants': liste_data})

# 3. Vue pour AJOUTER (avec gestion du groupe)
@csrf_exempt
@require_http_methods(["POST"])
def api_ajouter_etudiant(request):
    try:
        data = json.loads(request.body)
        
        # Récupération de la Promotion obligatoire
        promo = Promotion.objects.get(nom=data.get('promotion'))
        
        # Récupération du Groupe (optionnel dans le formulaire)
        groupe_nom = data.get('groupe')
        groupe_obj = None
        if groupe_nom and groupe_nom != "":
            # On cherche le groupe qui correspond au nom ET à la promotion
            groupe_obj = Groupe.objects.filter(nom=groupe_nom, promotion=promo).first()

        # Création de l'étudiant avec le lien vers le groupe
        Etudiant.objects.create(
            matricule=data.get('matricule'),
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            email=data.get('email'),
            promotion=promo,
            groupe=groupe_obj
        )
        return JsonResponse({"message": "Étudiant ajouté avec succès"}, status=201)
    except Promotion.DoesNotExist:
        return JsonResponse({"message": "Promotion introuvable"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

# 4. Vue pour SUPPRIMER
@csrf_exempt
@require_http_methods(["DELETE"])
def api_supprimer_etudiant(request, matricule):
    try:
        etu = Etudiant.objects.get(matricule=matricule)
        etu.delete()
        return JsonResponse({"message": "Supprimé"})
    except Etudiant.DoesNotExist:
        return JsonResponse({"message": "Non trouvé"}, status=404)

# 5. Vue pour les PROMOTIONS (remplissage menus déroulants)
def api_promotions_list(request):
    promos = list(Promotion.objects.values('id', 'nom'))
    return JsonResponse(promos, safe=False)

# 6. Vue pour les GROUPES
def api_groupes_list(request):
    groupes = list(Groupe.objects.values('id', 'nom', 'promotion__nom'))
    return JsonResponse(groupes, safe=False)
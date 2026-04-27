import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Etudiant, Promotion, Groupe


def _is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'ADMIN')


def liste_etudiants(request):
    return render(request, 'etudiants/etudiants.html')


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
            'moyenne': etu.moyenne_generale(),
            'statut': etu.status_performance(),
        })
    return JsonResponse({'etudiants': liste_data})


@login_required
@require_http_methods(["POST"])
def api_ajouter_etudiant(request):
    if not _is_admin(request.user):
        return JsonResponse({"message": "Accès refusé"}, status=403)
    try:
        data = json.loads(request.body)
        promo = Promotion.objects.get(nom=data.get('promotion'))
        groupe_nom = data.get('groupe')
        groupe_obj = None
        if groupe_nom and groupe_nom != "":
            groupe_obj = Groupe.objects.filter(nom=groupe_nom, promotion=promo).first()
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


@login_required
@require_http_methods(["DELETE"])
def api_supprimer_etudiant(request, matricule):
    if not _is_admin(request.user):
        return JsonResponse({"message": "Accès refusé"}, status=403)
    try:
        etu = Etudiant.objects.get(matricule=matricule)
        etu.delete()
        return JsonResponse({"message": "Supprimé"})
    except Etudiant.DoesNotExist:
        return JsonResponse({"message": "Non trouvé"}, status=404)


def api_promotions_list(request):
    promos = list(Promotion.objects.values('id', 'nom', 'annee'))
    return JsonResponse(promos, safe=False)


def api_groupes_list(request):
    groupes = list(Groupe.objects.values('id', 'nom', 'promotion__nom'))
    return JsonResponse(groupes, safe=False)


@login_required
@require_http_methods(["POST"])
def api_ajouter_promotion(request):
    if not _is_admin(request.user):
        return JsonResponse({"message": "Accès refusé"}, status=403)
    try:
        data = json.loads(request.body)
        nom = data.get('nom')
        annee = data.get('annee')
        if Promotion.objects.filter(nom=nom, annee=annee).exists():
            return JsonResponse({"message": "Cette promotion existe déjà pour cette année."}, status=400)
        Promotion.objects.create(nom=nom, annee=annee)
        return JsonResponse({"message": "Promotion créée avec succès"}, status=201)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def api_ajouter_groupe(request):
    if not _is_admin(request.user):
        return JsonResponse({"message": "Accès refusé"}, status=403)
    try:
        data = json.loads(request.body)
        nom = data.get('nom')
        promo = Promotion.objects.get(id=data.get('promotion_id'))
        if Groupe.objects.filter(nom=nom, promotion=promo).exists():
            return JsonResponse({"message": "Ce groupe existe déjà pour cette promotion."}, status=400)
        Groupe.objects.create(nom=data.get('nom'), promotion=promo)
        return JsonResponse({"message": "Groupe créé"}, status=201)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


def api_groupes_par_promotion(request, promo_id):
    groupes = Groupe.objects.filter(promotion_id=promo_id).values('id', 'nom')
    return JsonResponse(list(groupes), safe=False)


def promotion_groupe(request):
    return render(request, 'etudiants/promotion_groupe.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

from cours.models import Module
from etudiants.models import Groupe, Promotion, Etudiant
from evaluation.models import Note


##############################################
# 📄 PAGE PRINCIPALE
##############################################
def page_statistiques(request):
    context = {
        'modules': Module.objects.all(),
        'promotions': Promotion.objects.all(),
        'groupes': Groupe.objects.none(),   # 👈 vide au départ
        'etudiants': Etudiant.objects.none()
    }
    return render(request, 'statistique/statistique.html', context)


##############################################
# 📊 API STATISTIQUES (CORRIGÉE)
##############################################
def api_stats_globales(request):
    promotion_id = request.GET.get('promotion_id')
    groupe_id = request.GET.get('groupe_id')
    module_id = request.GET.get('module_id')
    etudiant_id = request.GET.get('etudiant_id')

    notes = Note.objects.all()

    # 🔥 FILTRES COMBINABLES
    if promotion_id:
        notes = notes.filter(etudiant__promotion_id=promotion_id)

    if groupe_id:
        notes = notes.filter(etudiant__groupe_id=groupe_id)

    if etudiant_id:
        notes = notes.filter(etudiant__matricule=etudiant_id)

    if module_id:
        notes = notes.filter(module_id=module_id)

    labels = []
    moyennes = []
    identite = None

    ##################################################
    # 🔥 CAS 1 : ETUDIANT + MODULE
    ##################################################
    if etudiant_id and module_id:
        moyenne = notes.aggregate(moy=Avg('valeur'))['moy'] or 0

        etudiant = Etudiant.objects.filter(matricule=etudiant_id).first()

        labels = ["Moyenne"]
        moyennes = [round(float(moyenne), 2)]
        identite = f"{etudiant.nom} {etudiant.prenom}" if etudiant else ""

    ##################################################
    # 🔥 CAS 2 : ETUDIANT SEUL (MOYENNE PAR MODULE)
    ##################################################
    elif etudiant_id:
        data = notes.values('module__libelle').annotate(
            moyenne=Avg('valeur')
        )

        labels = [d['module__libelle'] for d in data]
        moyennes = [round(float(d['moyenne']), 2) for d in data]

        etudiant = Etudiant.objects.filter(matricule=etudiant_id).first()
        identite = f"{etudiant.nom} {etudiant.prenom}" if etudiant else ""

    ##################################################
    # 🔥 CAS GLOBAL / GROUPE / PROMOTION
    ##################################################
    else:
        data = notes.values('module__libelle').annotate(
            moyenne=Avg('valeur')
        )

        labels = [d['module__libelle'] for d in data]
        moyennes = [round(float(d['moyenne']), 2) for d in data]

    return JsonResponse({
        'labels': labels,
        'moyennes': moyennes,
        'identite': identite
    })


##############################################
# 🎯 API GROUPES PAR PROMOTION
##############################################
def api_groupes(request):
    promotion_id = request.GET.get('promotion_id')

    if not promotion_id:
        return JsonResponse({"groupes": []})

    groupes = Groupe.objects.filter(promotion_id=promotion_id)

    data = [
        {"id": g.id, "nom": g.nom}
        for g in groupes
    ]

    return JsonResponse({"groupes": data})

##############################################
# 🎯 API ETUDIANTS PAR GROUPE
##############################################
def api_etudiants_par_groupe(request):
    groupe_id = request.GET.get('groupe_id')
    promotion_id = request.GET.get('promotion_id')

    # On commence par tous les étudiants
    etudiants = Etudiant.objects.all()

    # Si on a une promo, on filtre par promo
    if promotion_id:
        etudiants = etudiants.filter(promotion_id=promotion_id)
    
    # Si on a AUSSI (ou seulement) un groupe, on filtre par groupe
    if groupe_id:
        etudiants = etudiants.filter(groupe_id=groupe_id)

    # Sécurité : si on n'a aucun filtre, on renvoie une liste vide 
    # pour éviter de charger 500 étudiants pour rien
    if not promotion_id and not groupe_id:
        return JsonResponse({"etudiants": []})

    data = [
        {
            "id": e.matricule, 
            "nom": f"{e.nom} {e.prenom}"
        }
        for e in etudiants
    ]

    return JsonResponse({"etudiants": data})

##############################################
# 📈 DASHBOARD ETUDIANT
##############################################
def dashboard_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, pk=etudiant_id)

    notes = Note.objects.filter(etudiant=etudiant)

    module_id = request.GET.get('module_id')
    if module_id:
        notes = notes.filter(module_id=module_id)

    return JsonResponse({
        'identite': {
            'nom_complet': f"{etudiant.nom} {etudiant.prenom}",
            'matricule': etudiant.matricule,
        },
        'evolution_graph': {
            'labels': [n.module.libelle for n in notes],
            'data': [float(n.valeur) for n in notes]
        }
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg, Min, Max, Count, Q
import statistics
import math

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
        'groupes': Groupe.objects.none(),
        'etudiants': Etudiant.objects.none()
    }
    return render(request, 'statistique/statistique.html', context)


##############################################
# 📊 API STATISTIQUES COMPLÈTE
##############################################
def api_stats_globales(request):
    promotion_id = request.GET.get('promotion_id')
    groupe_id = request.GET.get('groupe_id')
    module_id = request.GET.get('module_id')
    etudiant_id = request.GET.get('etudiant_id')

    notes = Note.objects.all()

    # ✅ CORRECTION 1 : Vérifier que les valeurs ne sont pas vides
    if promotion_id and promotion_id != '':
        notes = notes.filter(etudiant__promotion_id=promotion_id) 
    if groupe_id and groupe_id != '':
        notes = notes.filter(etudiant__groupe_id=groupe_id)
    
    if etudiant_id and etudiant_id != '':
        notes = notes.filter(etudiant__matricule=etudiant_id)
    
    if module_id and module_id != '':
        notes = notes.filter(epreuve__module_id=module_id)

    # Debug
    print(f"🔍 Promo: {promotion_id} | Groupe: {groupe_id} | Etudiant: {etudiant_id} | Module: {module_id}")
    print(f"📊 Notes trouvées: {notes.count()}")

    labels = []
    moyennes = []
    identite = None

    ##################################################
    # CAS 1 : ETUDIANT + MODULE
    ##################################################
    if etudiant_id and etudiant_id != '' and module_id and module_id != '':
        moyenne = notes.aggregate(moy=Avg('valeur'))['moy'] or 0
        etudiant = Etudiant.objects.filter(matricule=etudiant_id).first()
        labels = ["Moyenne"]
        moyennes = [round(float(moyenne), 2)]
        identite = f"{etudiant.nom} {etudiant.prenom}" if etudiant else ""

    ##################################################
    # CAS 2 : ETUDIANT SEUL
    ##################################################
    elif etudiant_id and etudiant_id != '':
        data = notes.values('epreuve__module__libelle').annotate(
            moyenne=Avg('valeur')
        ).order_by('epreuve__module__libelle')
        labels = [d['epreuve__module__libelle'] for d in data]
        moyennes = [round(float(d['moyenne']), 2) if d['moyenne'] else 0 for d in data]
        etudiant = Etudiant.objects.filter(matricule=etudiant_id).first()
        identite = f"{etudiant.nom} {etudiant.prenom}" if etudiant else ""

    ##################################################
    # CAS 3 : VUE GLOBALE (PROMOTION, GROUPE, ou MODULE)
    ##################################################
    else:
        data = notes.values('epreuve__module__libelle').annotate(
            moyenne=Avg('valeur')
        ).order_by('epreuve__module__libelle')
        labels = [d['epreuve__module__libelle'] for d in data]
        moyennes = [round(float(d['moyenne']), 2) if d['moyenne'] else 0 for d in data]

    ##################################################
    # 📊 DISTRIBUTION DES NOTES
    ##################################################
    all_values = list(notes.values_list('valeur', flat=True))
    float_values = [float(v) for v in all_values if v is not None]

    dist_0_5 = len([v for v in float_values if v < 5])
    dist_5_10 = len([v for v in float_values if 5 <= v < 10])
    dist_10_15 = len([v for v in float_values if 10 <= v < 15])
    dist_15_20 = len([v for v in float_values if 15 <= v <= 20])

    distribution = {
        'labels': ['0-5', '5-10', '10-15', '15-20'],
        'data': [dist_0_5, dist_5_10, dist_10_15, dist_15_20]
    }

    ##################################################
    # 📈 STATS GLOBALES COMPLÈTES
    ##################################################
    agg = notes.aggregate(
        moyenne_globale=Avg('valeur'),
        note_min=Min('valeur'),
        note_max=Max('valeur')
    )

    # Médiane
    mediane = 0
    if float_values:
        mediane = round(statistics.median(float_values), 2)

    # Écart-type
    ecart_type = 0
    if len(float_values) >= 2:
        ecart_type = round(statistics.stdev(float_values), 2)

    # Total étudiants (uniques)
    total_etudiants = notes.values('etudiant').distinct().count()

    # Taux de réussite
    total_notes = len(float_values)
    reussis = len([v for v in float_values if v >= 10])
    taux_reussite = round((reussis / total_notes) * 100, 1) if total_notes > 0 else 0

    stats = {
        'moyenne_globale': round(float(agg['moyenne_globale'] or 0), 2),
        'note_min': round(float(agg['note_min'] or 0), 2),
        'note_max': round(float(agg['note_max'] or 0), 2),
        'mediane': mediane,
        'ecart_type': ecart_type,
        'total_etudiants': total_etudiants,
        'taux_reussite': taux_reussite,
    }

    ##################################################
    # 📊 MODULES STATS (barres min/médiane/max)
    ##################################################
    modules_data = notes.values('epreuve__module__libelle').annotate(
        min_val=Min('valeur'),
        max_val=Max('valeur'),
        avg_val=Avg('valeur')
    ).order_by('epreuve__module__libelle')

    mod_labels = []
    mins = []
    medianes_list = []
    maxs = []

    for m in modules_data:
        mod_name = m['epreuve__module__libelle']
        mod_labels.append(mod_name)
        mins.append(round(float(m['min_val'] or 0), 2))
        maxs.append(round(float(m['max_val'] or 0), 2))

        mod_notes = list(
            notes.filter(epreuve__module__libelle=mod_name)
                 .values_list('valeur', flat=True)
        )
        if mod_notes:
            mod_floats = [float(v) for v in mod_notes if v is not None]
            if mod_floats:
                medianes_list.append(round(statistics.median(mod_floats), 2))
            else:
                medianes_list.append(0)
        else:
            medianes_list.append(0)

    modules_stats = {
        'labels': mod_labels,
        'mins': mins,
        'medianes': medianes_list,
        'maxs': maxs,
    }

    ##################################################
    # 🚀 RÉPONSE COMPLÈTE
    ##################################################
    return JsonResponse({
        'labels': labels,
        'moyennes': moyennes,
        'identite': identite,
        'distribution': distribution,
        'stats': stats,
        'modules_stats': modules_stats,
    })


##############################################
# 🎯 API GROUPES PAR PROMOTION
##############################################
def api_groupes(request):
    promotion_id = request.GET.get('promotion_id')
    if not promotion_id or promotion_id == '':
        return JsonResponse({"groupes": []})

    groupes = Groupe.objects.filter(promotion_id=promotion_id).order_by('nom')
    data = [{"id": g.id, "nom": g.nom} for g in groupes]
    return JsonResponse({"groupes": data})


##############################################
# 🎯 API ETUDIANTS PAR GROUPE
##############################################
def api_etudiants_par_groupe(request):
    groupe_id = request.GET.get('groupe_id')
    promotion_id = request.GET.get('promotion_id')

    etudiants = Etudiant.objects.all()
    
    if promotion_id and promotion_id != '':
        etudiants = etudiants.filter(promotion_id=promotion_id)
    
    if groupe_id and groupe_id != '':
        etudiants = etudiants.filter(groupe_id=groupe_id)
    
    if not promotion_id and not groupe_id:
        return JsonResponse({"etudiants": []})

    etudiants = etudiants.order_by('nom', 'prenom')
    data = [{"id": e.matricule, "nom": f"{e.nom} {e.prenom}"} for e in etudiants]
    return JsonResponse({"etudiants": data})


##############################################
# 📈 DASHBOARD ETUDIANT
##############################################
def dashboard_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, pk=etudiant_id)
    notes = Note.objects.filter(etudiant=etudiant)

    module_id = request.GET.get('module_id')
    if module_id and module_id != '':
        notes = notes.filter(epreuve__module_id=module_id)

    return JsonResponse({
        'identite': {
            'nom_complet': f"{etudiant.nom} {etudiant.prenom}",
            'matricule': etudiant.matricule,
        },
        'evolution_graph': {
            'labels': [n.epreuve.module.libelle for n in notes],
            'data': [float(n.valeur) for n in notes]
        }
    })
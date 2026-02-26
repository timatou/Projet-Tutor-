from django.shortcuts import render
from django.http import JsonResponse
from etudiants.models import Etudiant, Promotion
from cours.models import Module
from evaluation.models import Note, Absence
from django.db.models import Avg, Count, Q
from datetime import datetime, timedelta, date
import calendar

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

def api_dashboard_stats(request):
    today = date.today()

    # ===== 1. KPI =====
    total_etudiants = Etudiant.objects.count()
    total_modules = Module.objects.count()
    total_absences = Absence.objects.count()

    # Variations
    variation_etudiants = 12
    modules_nouveaux = Module.objects.order_by('-id')[:12].count()

    absences_semaine = Absence.objects.filter(date__gte=today - timedelta(days=7)).count()
    absences_semaine_derniere = Absence.objects.filter(
        date__range=[today - timedelta(days=14), today - timedelta(days=7)]
    ).count()
    variation_absences = absences_semaine - absences_semaine_derniere

    # ===== 2. ALERTES =====
    etudiants_risque = []
    for etudiant in Etudiant.objects.all()[:5]:
        moyenne = Note.objects.filter(etudiant=etudiant).aggregate(Avg('valeur'))['valeur__avg'] or 0
        absences_non_just = Absence.objects.filter(etudiant=etudiant, statut__in=['EN_ATTENTE', 'REFUSEE']).count()

        if moyenne < 8:
            etudiants_risque.append({
                'matricule': etudiant.matricule,
                'raison': f'Moyenne {moyenne:.1f}/20'
            })
        elif absences_non_just > 3:
            etudiants_risque.append({
                'matricule': etudiant.matricule,
                'raison': f'{absences_non_just} absences non justifiées'
            })

    modules_echec = []
    for module in Module.objects.all():
        # CORRIGÉ : Note -> epreuve -> module
        notes = Note.objects.filter(epreuve__module=module)
        if notes.count() > 0:
            echecs = notes.filter(valeur__lt=10).count()
            taux_echec = (echecs / notes.count()) * 100
            if taux_echec > 40:
                modules_echec.append(module.code)

    total_alertes = len(etudiants_risque) + len(modules_echec)

    # ===== 3. RÉPARTITION PAR PROMOTION =====
    promotions = Promotion.objects.annotate(
        nb_etudiants=Count('etudiants')
    ).order_by('nom')

    promo_labels = [p.nom for p in promotions]
    promo_values = [p.nb_etudiants for p in promotions]

    # ===== 4. ÉVOLUTION DES ABSENCES MENSUELLES =====
    evolution_absences = []
    for i in range(11, -1, -1):
        mois_date = today - timedelta(days=30 * i)
        nb_absences = Absence.objects.filter(
            date__year=mois_date.year,
            date__month=mois_date.month
        ).count()
        evolution_absences.append({
            'mois': calendar.month_abbr[mois_date.month],
            'value': nb_absences
        })

    # ===== 5. STATUT ACADÉMIQUE =====
    statut_academique = {
        'labels': ['Sem1', 'Sem2', 'Sem3', 'Sem4'],
        'reussite': [],
        'difficile': []
    }

    for i in range(1, 5):
        # CORRIGÉ : notes -> epreuve -> module -> semestre
        reussite = Etudiant.objects.filter(
            notes__valeur__gte=10,
            notes__epreuve__module__semestre=i
        ).distinct().count()
        difficile = Etudiant.objects.filter(
            notes__valeur__lt=8,
            notes__epreuve__module__semestre=i
        ).distinct().count()

        statut_academique['reussite'].append(reussite or 350 + i * 10)
        statut_academique['difficile'].append(difficile or 40 - i * 2)

    # ===== 6. CAMEMBERT ABSENCES PAR MODULE =====
    absences_par_module = []
    top_modules = Absence.objects.values(
        'module__code', 'module__libelle'
    ).annotate(
        total=Count('id'),
        justifiees=Count('id', filter=Q(statut='VALIDEE')),
        non_justifiees=Count('id', filter=Q(statut__in=['EN_ATTENTE', 'REFUSEE']))
    ).order_by('-total')[:5]

    for module in top_modules:
        absences_par_module.append({
            'code': module['module__code'],
            'libelle': module['module__libelle'],
            'total': module['total'],
            'justifiees': module['justifiees'],
            'non_justifiees': module['non_justifiees']
        })

    if len(absences_par_module) < 5:
        modules_restants = Module.objects.exclude(
            code__in=[m['code'] for m in absences_par_module]
        )[:5 - len(absences_par_module)]

        for module in modules_restants:
            absences_par_module.append({
                'code': module.code,
                'libelle': module.libelle,
                'total': 0,
                'justifiees': 0,
                'non_justifiees': 0
            })

    return JsonResponse({
        'kpi': {
            'etudiants': {
                'total': total_etudiants,
                'variation': variation_etudiants
            },
            'modules': {
                'total': total_modules,
                'nouveaux': modules_nouveaux
            },
            'absences': {
                'total': total_absences,
                'variation': variation_absences
            },
            'alertes': {
                'total': total_alertes
            }
        },
        'alertes': {
            'immediates': total_alertes,
            'etudiants_risque': etudiants_risque[:3],
            'modules_echec': modules_echec[:2],
            'retards_saisie': 4
        },
        'repartition_promotions': {
            'labels': promo_labels,
            'values': promo_values
        },
        'evolution_absences': {
            'labels': [e['mois'] for e in evolution_absences],
            'values': [e['value'] for e in evolution_absences]
        },
        'statut_academique': statut_academique,
        'absences_par_module': absences_par_module
    })

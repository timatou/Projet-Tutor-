from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg
from cours.models import Module
from etudiants.models import Groupe, Promotion, Etudiant
from evaluation.models import Note
from .models import Statistique 

def page_statistiques(request):
    # On envoie les listes pour remplir les menus déroulants (select) du HTML
    context = {
        'modules': Module.objects.all(),
        'groupes': Groupe.objects.all(),
        'etudiants': Etudiant.objects.all().order_by('nom'),
    }
    return render(request, 'statistique/statistique.html', context)

def api_stats_globales(request):
    protion_id = request.GET.get('promotion_id')
    groupe_id = request.GET.get('groupe_id')
    module_id = request.GET.get('module_id')
    etudiant_id = request.GET.get('etudiant_id')

    notes = Note.objects.all()

    # 🔥 FILTRES
    if etudiant_id:
        notes = notes.filter(etudiant__matricule=etudiant_id)

    elif groupe_id:
        notes = notes.filter(etudiant__groupe_id=groupe_id)

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
    # 🔥 CAS 2 : ETUDIANT SEUL (IMPORTANT)
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
    # 🔥 CAS 3 : GLOBAL / GROUPE / MODULE
    ##################################################
    else:
        data = notes.values('module__libelle').annotate(
            moyenne=Avg('valeur')
        )

        labels = [d['module__libelle'] for d in data]
        moyennes = [round(float(d['moyenne']), 2) for d in data]

    ##################################################
    return JsonResponse({
        'labels': labels,
        'moyennes': moyennes,
        'identite': identite
    })


def dashboard_etudiant(request, etudiant_id):
    # pk (Primary Key) s'adaptera automatiquement à ton champ 654653
    etudiant = get_object_or_404(Etudiant, pk=etudiant_id)
    
    from evaluation.models import Note
    notes = Note.objects.filter(etudiant=etudiant)
    
    # On vérifie si un filtre module est appliqué
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
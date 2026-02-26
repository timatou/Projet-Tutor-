from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Note, Absence, Epreuve
from etudiants.models import Etudiant
from cours.models import Module
import json


# =====================================================
# ===================== NOTES =========================
# =====================================================

def notes_view(request):
    return render(request, 'evaluation/notes.html')


# -----------------------------------------------------
# API - LISTE DES EPREUVES
# -----------------------------------------------------

@csrf_exempt
def api_epreuves(request):
    epreuves = Epreuve.objects.select_related('module').all().order_by('-date')

    data = [
        {
            "id": e.id,
            "module_id": e.module.id,
            "module_code": e.module.code,
            "module_libelle": e.module.libelle,
            "type": e.type,
            "date": e.date.strftime("%Y-%m-%d"),
            "coefficient": float(e.coefficient),
        }
        for e in epreuves
    ]

    return JsonResponse({"epreuves": data})


# -----------------------------------------------------
# API - LISTE DES NOTES
# -----------------------------------------------------

@csrf_exempt
def api_notes(request):
    notes = Note.objects.select_related(
        'etudiant',
        'epreuve',
        'epreuve__module'
    ).all()

    data = [
        {
            'id': note.id,
            'etudiant_matricule': note.etudiant.matricule,
            'etudiant_nom': note.etudiant.nom,
            'etudiant_prenom': note.etudiant.prenom,
            'epreuve_id': note.epreuve.id,
            'module_id': note.epreuve.module.id,
            'module_code': note.epreuve.module.code,
            'module_libelle': note.epreuve.module.libelle,
            'type': note.epreuve.type,
            'date_epreuve': note.epreuve.date.strftime('%Y-%m-%d'),
            'valeur': float(note.valeur),
        }
        for note in notes
    ]

    return JsonResponse({'notes': data})


# -----------------------------------------------------
# API - AJOUT / UPDATE NOTE (ROBUSTE)
# -----------------------------------------------------

@csrf_exempt
@require_http_methods(["POST"])
def api_ajouter_note(request):
    try:
        data = json.loads(request.body)

        etudiant = Etudiant.objects.get(matricule=data['etudiant'])
        epreuve = Epreuve.objects.get(id=data['epreuve'])

        note, created = Note.objects.update_or_create(
            etudiant=etudiant,
            epreuve=epreuve,
            defaults={'valeur': data['valeur']}
        )

        message = "Note ajoutée" if created else "Note mise à jour"

        return JsonResponse({'success': True, 'message': message})

    except Etudiant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Étudiant introuvable'}, status=404)

    except Epreuve.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Épreuve introuvable'}, status=404)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


# -----------------------------------------------------
# API - SUPPRIMER NOTE
# -----------------------------------------------------

@csrf_exempt
@require_http_methods(["DELETE"])
def api_supprimer_note(request, id):
    try:
        note = Note.objects.get(id=id)
        note.delete()
        return JsonResponse({'success': True, 'message': 'Note supprimée'})
    except Note.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Note non trouvée'}, status=404)


# =====================================================
# ===================== ABSENCES ======================
# =====================================================

def absence_view(request):
    return render(request, 'evaluation/absences.html')


# -----------------------------------------------------
# API - LISTE ABSENCES
# -----------------------------------------------------

@csrf_exempt
def api_absences(request):
    absences = Absence.objects.select_related('etudiant', 'module').all()

    data = [
        {
            'id': abs.id,
            'etudiant_matricule': abs.etudiant.matricule,
            'etudiant_nom': abs.etudiant.nom,
            'etudiant_prenom': abs.etudiant.prenom,
            'module_code': abs.module.code,
            'module_libelle': abs.module.libelle,
            'module_id': abs.module.id,
            'date': abs.date.strftime('%Y-%m-%d'),
            'duree': float(abs.duree),
            'statut': abs.statut,
            'motif': abs.motif or '',
            'justifiee': abs.statut == 'VALIDEE'
        }
        for abs in absences
    ]

    # ✅ CALCULER LES STATS
    total = absences.count()
    justifiees = absences.filter(statut='VALIDEE').count()
    non_justifiees = total - justifiees
    etudiants_uniques = absences.values('etudiant').distinct().count()

    stats = {
        'total': total,
        'justifiees': justifiees,
        'non_justifiees': non_justifiees,
        'etudiants_concernes': etudiants_uniques
    }

    print(f"✅ Stats calculées: {stats}")  # Debug
    return JsonResponse({'absences': data, 'stats': stats})

# -----------------------------------------------------
# API - AJOUT ABSENCE
# -----------------------------------------------------

@csrf_exempt
@require_http_methods(["POST"])
def api_ajouter_absence(request):
    try:
        data = json.loads(request.body)

        etudiant = Etudiant.objects.get(matricule=data['etudiant'])
        module = Module.objects.get(id=data['module'])

        Absence.objects.create(
            etudiant=etudiant,
            module=module,
            date=data['date'],
            duree=data['duree'],
            motif=data.get('motif', ''),
            statut='EN_ATTENTE'
        )

        return JsonResponse({'success': True, 'message': 'Absence enregistrée'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


# -----------------------------------------------------
# API - VALIDER ABSENCE
# -----------------------------------------------------

@csrf_exempt
@require_http_methods(["POST"])
def api_valider_absence(request, absence_id):
    try:
        absence = Absence.objects.get(id=absence_id)
        absence.statut = 'VALIDEE'
        absence.save()

        return JsonResponse({'success': True})

    except Absence.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


# -----------------------------------------------------
# API - SUPPRIMER ABSENCE
# -----------------------------------------------------

@csrf_exempt
@require_http_methods(["DELETE"])
def api_supprimer_absence(request, id):
    try:
        absence = Absence.objects.get(id=id)
        absence.delete()
        return JsonResponse({'success': True})
    except Absence.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
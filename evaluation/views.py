from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Note, Absence
from etudiants.models import Etudiant
from cours.models import Module
import json

# ===============================
# VUES POUR LES NOTES
# ===============================

def notes_view(request):
    """Affiche la page de gestion des notes"""
    return render(request, 'evaluation/notes.html')

def ajouter_note(request):
    """Vue pour afficher le formulaire d'ajout de note"""
    return render(request, 'evaluation/ajouter_note.html')

@csrf_exempt
def api_notes(request):
    """API pour récupérer la liste des notes"""
    notes = Note.objects.select_related('etudiant', 'module').all()
    
    data = []
    for note in notes:
        data.append({
            'id': note.id,
            'etudiant_matricule': note.etudiant.matricule,
            'etudiant_nom': note.etudiant.nom,
            'etudiant_prenom': note.etudiant.prenom,
            'module_id': note.module.id,
            'module_code': note.module.code,
            'module_libelle': note.module.libelle,
            'type': note.type,
            'valeur': note.valeur,
            'date': note.date.strftime('%Y-%m-%d'),
        })
    
    return JsonResponse({'notes': data})

@csrf_exempt
@require_http_methods(["POST"])
def api_ajouter_note(request):
    """API pour ajouter une note"""
    try:
        data = json.loads(request.body)
        
        etudiant = Etudiant.objects.get(matricule=data['etudiant'])
        module = Module.objects.get(id=data['module'])
        
        note = Note.objects.create(
            etudiant=etudiant,
            module=module,
            type=data['type'],
            valeur=data['valeur'],
            date=data.get('date')
        )
        
        return JsonResponse({
            'success': True,
            'id': note.id,
            'message': 'Note ajoutée avec succès'
        })
    except Etudiant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Étudiant non trouvé'}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Module non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def api_modifier_note(request, id):
    """API pour modifier une note"""
    try:
        data = json.loads(request.body)
        note = Note.objects.get(id=id)
        
        # Mettre à jour les champs
        if 'etudiant' in data:
            note.etudiant = Etudiant.objects.get(matricule=data['etudiant'])
        if 'module' in data:
            note.module = Module.objects.get(id=data['module'])
        if 'type' in data:
            note.type = data['type']
        if 'valeur' in data:
            note.valeur = data['valeur']
        if 'date' in data:
            note.date = data['date']
        
        note.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Note modifiée avec succès'
        })
    except Note.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Note non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_supprimer_note(request, id):
    """API pour supprimer une note"""
    try:
        note = Note.objects.get(id=id)
        note.delete()
        return JsonResponse({'success': True, 'message': 'Note supprimée'})
    except Note.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Note non trouvée'}, status=404)

# ===============================
# VUES POUR LES ABSENCES
# ===============================

def absence_view(request):
    """Affiche la page de gestion des absences"""
    return render(request, 'evaluation/absences.html')

def saisir_absence(request):
    """Vue pour afficher le formulaire de saisie d'absence"""
    return render(request, 'evaluation/saisir_absence.html')

@csrf_exempt
def api_absences(request):
    """API pour récupérer la liste des absences avec filtres"""
    absences = Absence.objects.select_related('etudiant', 'module').all()
    
    # Filtres
    etudiant_id = request.GET.get('etudiant')
    module_id = request.GET.get('module')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    if etudiant_id:
        absences = absences.filter(etudiant__matricule=etudiant_id)
    if module_id:
        absences = absences.filter(module_id=module_id)
    if date_debut:
        absences = absences.filter(date__gte=date_debut)
    if date_fin:
        absences = absences.filter(date__lte=date_fin)
    
    data = []
    for abs in absences:
        data.append({
            'id': abs.id,
            'etudiant_id': abs.etudiant.matricule,
            'etudiant_matricule': abs.etudiant.matricule,
            'etudiant_nom': abs.etudiant.nom,
            'etudiant_prenom': abs.etudiant.prenom,
            'module_id': abs.module.id,
            'module_code': abs.module.code,
            'module_libelle': abs.module.libelle,
            'date': abs.date.strftime('%Y-%m-%d'),
            'duree': float(abs.duree),
            'justifiee': abs.justifiee,
            'motif': abs.motif or ''
        })
    
    # Statistiques
    total = absences.count()
    justifiees = absences.filter(justifiee=True).count()
    non_justifiees = absences.filter(justifiee=False).count()
    etudiants_concernes = absences.values('etudiant').distinct().count()
    
    stats = {
        'total': total,
        'justifiees': justifiees,
        'non_justifiees': non_justifiees,
        'etudiants_concernes': etudiants_concernes
    }
    
    return JsonResponse({'absences': data, 'stats': stats})

@csrf_exempt
@require_http_methods(["POST"])
def api_ajouter_absence(request):
    """API pour ajouter une absence"""
    try:
        data = json.loads(request.body)
        
        # Récupérer l'étudiant par son matricule
        etudiant = Etudiant.objects.get(matricule=data['etudiant'])
        module = Module.objects.get(id=data['module'])
        
        absence = Absence.objects.create(
            etudiant=etudiant,
            module=module,
            date=data['date'],
            duree=data['duree'],
            motif=data.get('motif', ''),
            justifiee=False
        )
        
        return JsonResponse({
            'success': True, 
            'id': absence.id,
            'message': 'Absence enregistrée avec succès'
        })
    except Etudiant.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Étudiant non trouvé'
        }, status=404)
    except Module.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Module non trouvé'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_justifier_absence(request, absence_id):
    """API pour justifier une absence"""
    try:
        # Récupérer l'absence
        absence = Absence.objects.get(id=absence_id)
        
        # Marquer comme justifiée
        absence.justifiee = True
        absence.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Absence justifiée avec succès'
        })
        
    except Absence.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Absence non trouvée'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_supprimer_absence(request, id):
    """API pour supprimer une absence"""
    try:
        absence = Absence.objects.get(id=id)
        absence.delete()
        return JsonResponse({
            'success': True,
            'message': 'Absence supprimée avec succès'
        })
    except Absence.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Absence non trouvée'
        }, status=404)
@csrf_exempt
@require_http_methods(["PUT"])
def api_modifier_absence(request, id):
    """API pour modifier une absence"""
    try:
        data = json.loads(request.body)
        absence = Absence.objects.get(id=id)
        
        # Mettre à jour les champs
        if 'module' in data:
            absence.module = Module.objects.get(id=data['module'])
        if 'date' in data:
            absence.date = data['date']
        if 'duree' in data:
            absence.duree = data['duree']
        if 'motif' in data:
            absence.motif = data['motif']
        
        absence.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Absence modifiée avec succès'
        })
    except Absence.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Absence non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
from django.shortcuts import render, redirect
from .forms import NoteForm, AbsenceForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Note
from .models import Absence
import json
from django.views.decorators.csrf import csrf_exempt


def est_professeur(user):
    return user.groups.filter(name='Professeurs').exists() or user.is_superuser

@login_required
@user_passes_test(est_professeur)

def ajouter_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save() # Enregistre la note en base de données
            return redirect('liste_etudiants') # Redirection après succès
    else:
        form = NoteForm()
    
    return render(request, 'evaluation/saisie_note.html', {'form': form})

def saisir_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save() # Enregistrement de l'absence 
            return redirect('liste_etudiants')
    else:
        form = AbsenceForm()
    
    return render(request, 'evaluation/saisie_absence.html', {'form': form})


@csrf_exempt
def api_ajouter_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        note = Note.objects.create(
            etudiant_id=data["etudiant"],
            module_id=data["module"],
            valeur=data["valeur"],
            type=data["TYPE_CHOICES"],
            date=data["date"]
        )
        return JsonResponse({"success": True, "id": note.id})


@csrf_exempt
def api_ajouter_absence(request):
    if request.method == "POST":
        data = json.loads(request.body)
        absence =Absence.objects.create(
            etudiant_id=data["etudiant"],
            module_id=data["module"],
            date=data["date"],
            duree=data["duree"],
            justifiee=data["justifiee"],
            motif=data.get("motif", "")
        )
        return JsonResponse({"success": True, "id": absence.id})
    

def api_notes(request):
    notes = Note.objects.select_related('etudiant', 'module')

    data = []
    for n in notes:
        data.append({
            "id": n.id,
            "etudiant": str(n.etudiant),
            "module": str(n.module),
            "valeur": n.valeur,
            "type": n.type,
            "date": n.date.isoformat()
        })

    return JsonResponse({"notes": data})


@csrf_exempt
def api_ajouter_note(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Vérifie bien que ces noms correspondent à ton models.py
            note = Note.objects.create(
                etudiant_id=data.get("etudiant"), # ID ou Matricule ?
                module_id=data.get("module"),     # ID du module envoyé par le Select
                valeur=data.get("valeur"),
                type=data.get("type"),       # C'est 'type' dans le JSON JS
                date=data.get("date")             # C'est 'date' dans le JSON JS
            )
            return JsonResponse({"success": True})
        except Exception as e:
            # ICI : On renvoie l'erreur réelle pour t'aider à débugger
            return JsonResponse({"success": False, "error": str(e)}, status=400)

# evaluation/views.py

def notes_view(request):
    # Cette vue sert juste à charger la page HTML 
    # Ton JavaScript fera ensuite le travail de récupérer le JSON
    return render(request, 'evaluation/notes.html')


@csrf_exempt # Pour autoriser la requête DELETE sans formulaire classique
def api_supprimer_note(request, id):
    if request.method == "DELETE":
        try:
            note = Note.objects.get(id=id)
            note.delete()
            return JsonResponse({"success": True, "message": "Note supprimée"})
        except Note.DoesNotExist:
            return JsonResponse({"success": False, "error": "Note introuvable"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



def api_absences(request):
    absences = Absence.objects.select_related('etudiant', 'module')

    data = []
    for n in absences:
        data.append({
            "id": n.id,
            "etudiant": str(n.etudiant),
            "module": str(n.module),
            "date_absence": n.date.isoformat(),
            "duree": str(n.duree),
            "justifiee": n.justifiee,
            "motif": n.motif

        })

    return JsonResponse({"absences": data})

@csrf_exempt
def api_ajouter_absence(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Vérifie bien que ces noms correspondent à ton models.py
            absence = Absence.objects.create(
                etudiant_id=data.get("etudiant"), # ID ou Matricule ?
                module_id=data.get("module"),     # ID du module envoyé par le Select
                date=data["date"],
                duree=data["duree"],
                justifiee=data["justifiee"],
                motif=data.get("motif", "")
            )
            return JsonResponse({"success": True, "id": absence.id})
        except Exception as e:
            print(f"ERREUR API : {e}") # <--- AJOUTE ÇA : L'erreur s'affichera dans ton terminal noir
            return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt # Pour autoriser la requête DELETE sans formulaire classique
def api_supprimer_absence(request, id):
    if request.method == "DELETE":
        try:
            absence = Absence.objects.get(id=id)
            absence.delete()
            return JsonResponse({"success": True, "message": "Absence supprimée"})
        except Absence.DoesNotExist:
            return JsonResponse({"success": False, "error": "Absence introuvable"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



def absence_view(request):
    # Cette vue sert juste à charger la page HTML 
    # Ton JavaScript fera ensuite le travail de récupérer le JSON
    return render(request, 'evaluation/absences.html')

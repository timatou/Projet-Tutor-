from django.shortcuts import render, redirect
from .forms import NoteForm, AbsenceForm
from django.contrib.auth.decorators import login_required, user_passes_test

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
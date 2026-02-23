from django.shortcuts import render, redirect
from .models import Professeur
from .forms import ProfesseurRegistrationForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Professeur
from .forms import ProfesseurUpdateForm

def editer_enseignant(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)
    if request.method == 'POST':
        form = ProfesseurUpdateForm(request.POST, instance=professeur)
        if form.is_valid():
            form.save()
            return redirect('liste_enseignants')
        # Si INVALIDE, il sort du IF et va vers le RENDER en bas avec les erreurs
    else:
        form = ProfesseurUpdateForm(instance=professeur)
    
    return render(request, 'utilisateurs/editer_enseignant.html', {'form': form, 'professeur': professeur})

def ajouter_enseignant(request):
    if request.method == 'POST':
        form = ProfesseurRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_enseignants')
    else:
        form = ProfesseurRegistrationForm()
    
    return render(request, 'utilisateurs/ajouter_enseignant.html', {'form': form})
def liste_enseignants(request):
    # On récupère les profs, leur compte User, ET leurs modules associés
    profs = Professeur.objects.select_related('user').prefetch_related('modules').all()
    return render(request, 'utilisateurs/enseignants.html', {'profs': profs})

def dashboard_redirect(request):
    """ Redirection après connexion selon le rôle """
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role == 'ADMIN':
        return redirect('liste_enseignants') # L'admin voit les profs
    else:
        return redirect('liste_notes') # Le prof voit les notes
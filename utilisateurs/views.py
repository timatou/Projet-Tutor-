from django.shortcuts import render, redirect
from .models import Professeur
from .forms import ProfesseurRegistrationForm
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProfesseurUpdateForm
from django.contrib.auth.decorators import login_required
from cours.models import Module  
from evaluation.models import Note, Epreuve
from etudiants.models import Etudiant
from evaluation.models import Absence

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

@login_required
def dashboard_redirect(request):
    # Si c'est le superutilisateur (il a tous les droits)
    if request.user.is_superuser or request.user.role == 'ADMIN':
        return redirect('liste_enseignants')
    
    # Si c'est un enseignant
    elif request.user.role == 'PROFESSEUR':
        return redirect('espace_enseignant')
    
    # Sécurité : si le rôle est inconnu, renvoyer vers une page par défaut
    return redirect('login')

@login_required
def espace_enseignant(request):
    # On initialise les variables pour éviter des erreurs dans le template
    mes_modules = []
    has_modules = False
    
    # On essaie de récupérer le profil professeur attaché à l'utilisateur
    # Teste 'professeur' si 'professeur_profile' ne marche pas
    professeur = getattr(request.user, 'professeur_profile', None) or getattr(request.user, 'professeur', None)
    
    if professeur:
        mes_modules = professeur.modules.all()
        has_modules = mes_modules.exists()
    
    return render(request, 'utilisateurs/espace_enseignant.html', {
        'modules': mes_modules,
        'has_modules': has_modules
    })

@login_required
def saisir_notes_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, professeurs__user=request.user)
    # Filtrer les étudiants des promotions assignées au module
    etudiants = Etudiant.objects.filter(promotion__in=module.promotions.all()).select_related('promotion', 'groupe') 

    if request.method == 'POST':
        type_eval = request.POST.get('type_evaluation')
        date_examen = request.POST.get('date_examen')
        
        # Créer ou récupérer l'épreuve
        epreuve, created = Epreuve.objects.get_or_create(
            module=module,
            type=type_eval,
            date=date_examen,
            defaults={'coefficient': 1.0}  # Valeur par défaut
        )
        
        for etudiant in etudiants:
            valeur = request.POST.get(f'note_{etudiant.pk}')
            
            if valeur and valeur.strip() != "":
                try:
                    note_float = float(valeur.replace(',', '.'))
                    
                    # Créer ou mettre à jour la note pour cette épreuve
                    Note.objects.update_or_create(
                        etudiant=etudiant,
                        epreuve=epreuve,
                        defaults={'valeur': note_float}
                    )
                except ValueError:
                    continue
        
        return redirect('espace_enseignant')

    return render(request, 'utilisateurs/saisie_masse_notes.html', {
        'module': module,
        'etudiants': etudiants,
        'types': Epreuve.TYPE_CHOICES
    })

 # Assure-toi d'importer le modèle Absence

@login_required
def faire_appel_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, professeurs__user=request.user)
    # Filtrer les étudiants des promotions assignées au module
    etudiants = Etudiant.objects.filter(promotion__in=module.promotions.all()).select_related('promotion', 'groupe')

    if request.method == 'POST':
        date_appel = request.POST.get('date_absence')
        duree_cours = request.POST.get('duree_heures')
        
        for etudiant in etudiants:
            # On vérifie si la case "absent_ID" a été cochée
            is_absent = request.POST.get(f'absent_{etudiant.pk}')
            
            if is_absent:
                Absence.objects.get_or_create(
                    etudiant=etudiant,
                    module=module,
                    date=date_appel,
                    defaults={
                        'duree': duree_cours,
                        'justifiee': False,
                        'motif': 'Appel en classe'
                    }
                )
        return redirect('espace_enseignant')

    return render(request, 'utilisateurs/faire_appel.html', {
        'module': module,
        'etudiants': etudiants
    })
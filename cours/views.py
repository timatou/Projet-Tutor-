import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Module
from django.contrib.auth.decorators import login_required
from .models import Module
from  evaluation.models import Note
from .forms import ModuleUpdateForm
# Affiche la page HTML
def liste_modules(request):
    return render(request, 'cours/modules.html')

# Envoie les données au JavaScript
def api_modules_data(request):
    # FILTRAGE : Si c'est un prof, on restreint la liste à ses modules uniquement
    if request.user.is_authenticated and request.user.role == 'PROFESSEUR':
        modules = Module.objects.filter(professeurs__user=request.user).prefetch_related('professeurs')
    else:
        # L'admin ou le superuser voit tout
        modules = Module.objects.prefetch_related('professeurs').all()

    liste_data = []
    for m in modules:
        profs_noms = ", ".join([str(p) for p in m.professeurs.all()])
        
        liste_data.append({
            'id': m.id,
            'code': m.code,
            'libelle': m.libelle,
            'coefficient': m.coefficient,
            'semestre': m.semestre,
            'professeurs': profs_noms if profs_noms else "Non assigné",
            'moyenne': m.calculer_moyenne(),
            'taux': m.taux_reussite(),
        })
    
    return JsonResponse({'modules': liste_data})
# Ajoute un module en base
@csrf_exempt
def api_ajouter_module(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            Module.objects.create(
                code=data.get('code'),
                libelle=data.get('libelle'),
                coefficient=data.get('coefficient'),
                semestre=data.get('semestre')
            )
            return JsonResponse({"message": "Succès"}, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"message": "Méthode non autorisée"}, status=405)

# Supprime un module
@csrf_exempt
def api_supprimer_module(request, module_id):
    if request.method == "DELETE":
        try:
            m = Module.objects.get(id=module_id)
            m.delete()
            return JsonResponse({"message": "Supprimé"})
        except Module.DoesNotExist:
            return JsonResponse({"message": "Non trouvé"}, status=404)

@login_required
def liste_notes(request):
    if request.user.role == 'ADMIN':
        # L'admin voit tout
        notes = Note.objects.all()
    else:
        # Le professeur ne voit que les notes des modules qu'IL enseigne
        # On remonte via : Note -> Module -> Professeur -> User
        notes = Note.objects.filter(module__professeur__user=request.user)
    
    return render(request, 'cours/liste_notes.html', {'notes': notes})

@login_required
def editer_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ModuleUpdateForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('liste_modules')
    else:
        form = ModuleUpdateForm(instance=module)
    
    return render(request, 'cours/editer_module.html', {'form': form, 'module': module})

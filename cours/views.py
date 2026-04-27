import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Module
from evaluation.models import Note
from .forms import ModuleUpdateForm


def _is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'ADMIN')


def liste_modules(request):
    return render(request, 'cours/modules.html')


def api_modules_data(request):
    if request.user.is_authenticated and request.user.role == 'PROFESSEUR':
        modules = Module.objects.filter(professeurs__user=request.user).prefetch_related('professeurs')
    else:
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


@login_required
def api_ajouter_module(request):
    if not _is_admin(request.user):
        return JsonResponse({"message": "Accès refusé"}, status=403)
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


@login_required
def api_supprimer_module(request, module_id):
    if not _is_admin(request.user):
        return JsonResponse({"message": "Accès refusé"}, status=403)
    if request.method == "DELETE":
        try:
            m = Module.objects.get(id=module_id)
            m.delete()
            return JsonResponse({"message": "Supprimé"})
        except Module.DoesNotExist:
            return JsonResponse({"message": "Non trouvé"}, status=404)
    return JsonResponse({"message": "Méthode non autorisée"}, status=405)


@login_required
def liste_notes(request):
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        notes = Note.objects.all()
    else:
        notes = Note.objects.filter(epreuve__module__professeurs__user=request.user)
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

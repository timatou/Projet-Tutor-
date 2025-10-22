from django.contrib import admin
from django.urls import path
from django.shortcuts import render


# ==============================
# VUES SIMPLES (affichent les templates du dossier frontend/templates)
# ==============================


def login_view(request):
    return render(request, "login.html")


def dashboard_view(request):
    return render(request, "dashboard.html")


def etudiants_view(request):
    return render(request, "etudiants.html")


def modules_view(request):
    return render(request, "modules.html")


def notes_view(request):
    return render(request, "notes.html")


def absences_view(request):
    return render(request, "absences.html")


def statistiques_view(request):
    return render(request, "statistiques.html")


# ==============================
# ROUTES (URLs)
# ==============================
urlpatterns = [
    path("admin/", admin.site.urls),
    # Accueil = page de connexion
    path("", login_view, name="login"),
    # Pages internes
    path("dashboard/", dashboard_view, name="dashboard"),
    path("etudiants/", etudiants_view, name="etudiants"),
    path("modules/", modules_view, name="modules"),
    path("notes/", notes_view, name="notes"),
    path("absences/", absences_view, name="absences"),
    path("statistiques/", statistiques_view, name="statistiques"),
]

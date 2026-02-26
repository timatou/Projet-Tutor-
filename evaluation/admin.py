from django.contrib import admin
from .models import Epreuve, Note, Absence


# ============================
#        EPREUVE ADMIN
# ============================

@admin.register(Epreuve)
class EpreuveAdmin(admin.ModelAdmin):
    list_display = ('module', 'type', 'date', 'coefficient')
    list_filter = ('module', 'type', 'date')
    search_fields = ('module__libelle',)


# ============================
#        NOTE ADMIN
# ============================

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'epreuve', 'valeur', 'est_reussie')
    list_filter = ('epreuve',)
    search_fields = ('etudiant__nom', 'etudiant__prenom')
    autocomplete_fields = ['etudiant', 'epreuve']


# ============================
#        ABSENCE ADMIN
# ============================

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'module', 'date', 'duree', 'statut')
    list_filter = ('statut', 'module', 'date')
    search_fields = ('etudiant__nom', 'etudiant__prenom')
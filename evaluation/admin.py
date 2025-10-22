#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Note, Absence  # importe tes modèles ici

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'module', 'type', 'valeur', 'date')
    list_filter = ('type', 'module', 'date')
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'module__libelle')

@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'module', 'date', 'justifiee')
    list_filter = ('justifiee', 'date', 'module')
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'module__libelle')

from django.contrib import admin
from .models import Module

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle', 'coefficient', 'semestre', 'get_moyenne', 'get_reussite')
    list_filter = ('semestre',)
    search_fields = ('code', 'libelle')
    
    # Ajout des indicateurs de performance dans la liste
    def get_moyenne(self, obj):
        return f"{obj.calculer_moyenne()} / 20"
    get_moyenne.short_description = 'Moyenne Globale'

    def get_reussite(self, obj):
        return f"{obj.taux_reussite()}%"
    get_reussite.short_description = 'Taux de Réussite'
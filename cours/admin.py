from django.contrib import admin
from .models import Module

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'libelle', 'coefficient', 'semestre',
        'afficher_professeurs', 'get_moyenne', 'get_reussite'
    )
    list_filter = ('semestre',)
    search_fields = ('code', 'libelle')
    filter_horizontal = ('professeurs', 'etudiants')

    def afficher_professeurs(self, obj):
        return ", ".join(str(p) for p in obj.professeurs.all())
    afficher_professeurs.short_description = "Professeurs"

    @admin.display(description="Moyenne Globale")
    def get_moyenne(self, obj):
        return f"{obj.calculer_moyenne()} / 20"

    @admin.display(description="Taux de Réussite")
    def get_reussite(self, obj):
        return f"{obj.taux_reussite()}%"

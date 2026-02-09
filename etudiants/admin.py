from django.contrib import admin
from django.utils.html import format_html # Import indispensable pour les couleurs
from .models import Promotion, Groupe, Etudiant

# Optionnel : Personnalisation du titre de l'interface
admin.site.site_header = "Gestion du Projet Tutoré"
admin.site.index_title = "Tableau de Bord Backend"

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee')
    search_fields = ('nom',)

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'promotion')
    list_filter = ('promotion',)
    # Permet de chercher un groupe par son nom ou le nom de sa promotion
    search_fields = ('nom', 'promotion__nom') 

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    # 1. Optimisation : charge les relations en une seule requête (évite de ramer)
    list_select_related = ('promotion', 'groupe')

    # 2. Affichage de la liste
    list_display = ('nom', 'prenom', 'promotion', 'groupe', 'get_moyenne', 'status_performance_display')
    list_filter = ('promotion', 'groupe')
    search_fields = ('nom', 'prenom', 'email')
    
    # 3. Organisation du formulaire de modification (Fiche Étudiant)
    fieldsets = (
        ('Informations Personnelles', {
            'fields': (('nom', 'prenom'), 'email') # Met nom et prénom sur la même ligne
        }),
        ('Affectation', {
            'fields': ('promotion', 'groupe')
        }),
    )

    # --- Méthodes calculées ---

    def get_moyenne(self, obj):
        val = obj.moyenne_generale()
        return f"{val} / 20"
    get_moyenne.short_description = 'Moyenne'
    get_moyenne.admin_order_field = 'moyenne' # Permet de trier par moyenne si le champ existe

    def status_performance_display(self, obj):
        status = obj.status_performance()
        
        # Personnalisation des couleurs selon le texte renvoyé
        # On suppose que ton modèle renvoie "Admis", "Ajourné" ou "Excellent"
        color = "black"
        if "Admis" in status or "Excellent" in status:
            color = "#28a745" # Vert
        elif "Ajourné" in status or "Échec" in status:
            color = "#dc3545" # Rouge
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_performance_display.short_description = 'Performance'
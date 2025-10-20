from django.contrib import admin

# Register your models here.
from .models import Promotion, Groupe, Etudiant

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee')

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'promotion')
    list_filter = ('promotion',)

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'promotion', 'groupe')
    list_filter = ('promotion', 'groupe')
    search_fields = ('nom', 'prenom', 'email')
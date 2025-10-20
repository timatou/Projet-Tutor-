from django.contrib import admin
from .models import Promotion, Groupe, Etudiant
# Register your models here.

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
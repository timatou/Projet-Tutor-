from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Professeur, Administrateur, Etudiant

# Permet d'afficher les champs du profil directement dans la fiche User
class ProfesseurInline(admin.StackedInline):
    model = Professeur
    can_delete = False
    verbose_name_plural = 'Détails du Profil Professeur'

class AdministrateurInline(admin.StackedInline):
    model = Administrateur
    can_delete = False
    verbose_name_plural = 'Détails du Profil Admin'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # On ajoute les inlines pour voir les profils dans la fiche utilisateur
    inlines = (ProfesseurInline, AdministrateurInline)
    
    list_display = ('username', 'email', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    # On ajoute le champ rôle dans l'édition de l'utilisateur
    fieldsets = UserAdmin.fieldsets + (
        ('Attribution du Rôle', {'fields': ('role',)}),
    )

# On garde les enregistrements individuels si besoin
admin.site.register(Professeur)
admin.site.register(Administrateur)
admin.site.register(Etudiant)
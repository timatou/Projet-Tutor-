from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Professeur, Administrateur

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle', {'fields': ('role',)}),
    )

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite')

@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'departement')
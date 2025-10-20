from django.contrib import admin
from .models import Module

# Register your models here.

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle', 'coefficient', 'semestre', 'enseignant', 'promotion')
    list_filter = ('semestre', 'promotion')
    search_fields = ('code', 'libelle')

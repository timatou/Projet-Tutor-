from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    libelle = models.CharField(max_length=100)
    coefficient = models.FloatField(default=1.0)
    semestre = models.IntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(10)]
)
    # Relations
    professeurs = models.ManyToManyField('utilisateurs.Professeur', related_name='modules',blank=True)
    etudiants = models.ManyToManyField('utilisateurs.Etudiant', related_name='modules',blank=True)

    def __str__(self):
        return f"{self.libelle} (S{self.semestre})"

    def calculer_moyenne(self):
        from evaluation.models import Note
        notes = Note.objects.filter(module=self).aggregate(Avg('valeur'))
        moyenne = notes['valeur__avg']
        return round(moyenne, 2) if moyenne is not None else 0
    
    def taux_reussite(self):
        from evaluation.models import Note
        notes = Note.objects.filter(module=self)
        if not notes.exists():
            return 0
        reussites = notes.filter(valeur__gte=10).count() # Note >= 10/20
        return round((reussites / notes.count()) * 100, 2)

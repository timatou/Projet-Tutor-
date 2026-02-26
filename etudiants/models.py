from django.db import models
from django.db.models import Avg

# ----- Classe Promotion -----
class Promotion(models.Model):
    nom = models.CharField(max_length=100)
    annee = models.CharField(max_length=9)  

    class Meta:
        # Empêche d'avoir deux fois "L3 Info" pour "2025-2026"
        unique_together = ('nom', 'annee')

    def __str__(self):
        return f"{self.nom} {self.annee}"


# ----- Classe Groupe -----
class Groupe(models.Model):
    nom = models.CharField(max_length=50)
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='groupes'
    )
    class Meta:
        # Empêche d'avoir deux fois "Groupe A" pour la même promotion
        unique_together = ('nom', 'promotion')

    def __str__(self):
        return f"{self.nom} ({self.promotion})"


# ----- Classe Étudiant -----
class Etudiant(models.Model):
    matricule = models.CharField(max_length=13, unique=True, primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='etudiants'
    )
    groupe = models.ForeignKey(
        Groupe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etudiants'
    )

    def __str__(self):
        return f" {self.matricule}"

    def moyenne_generale(self):
        notes = self.notes.all()
        if not notes.exists():
            return 0.0
        moyenne = notes.aggregate(Avg('valeur'))['valeur__avg']
        return round(moyenne, 2)
    
    def status_performance(self):
        moyenne = self.moyenne_generale()
        if moyenne < 8 :
            return "Rouge"
        elif moyenne < 10 :
            return "Orange"
        return "Vert"
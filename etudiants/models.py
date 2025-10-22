from django.db import models


# ----- Classe Promotion -----
class Promotion(models.Model):
    nom = models.CharField(max_length=100)
    annee = models.CharField(max_length=9)  # Format attendu : "2024-2025"

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

    def __str__(self):
        return f"{self.nom} - {self.promotion}"


# ----- Classe Étudiant -----
class Etudiant(models.Model):
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
        return f"{self.prenom} {self.nom}"

    def moyenne_generale(self):
        # Cette méthode calculera plus tard la moyenne de l'étudiant
        return 0.0

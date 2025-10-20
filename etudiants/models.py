from django.db import models

# Create your models here.

class Promotion(models.Model):
    nom = models.CharField(max_length=100)
    annee = models.CharField(max_length=9)  # Format: "2024-2025"
    
    def _str_(self):
        return f"{self.nom} {self.annee}"

class Groupe(models.Model):
    nom = models.CharField(max_length=50)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    
    def _str_(self):
        return f"{self.nom} - {self.promotion}"

class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.SET_NULL, null=True, blank=True)
    
    def _str_(self):
        return f"{self.prenom} {self.nom}"
    
    def moyenne_generale(self):
        # À implémenter plus tard
        return 0.0
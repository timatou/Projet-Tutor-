from django.db import models

# Create your models here.
class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    libelle = models.CharField(max_length=100)
    coefficient = models.FloatField(default=1.0)
    semestre = models.IntegerField()
    enseignant = models.ForeignKey('utilisateurs.Professeur', on_delete=models.SET_NULL, null=True)
    promotion = models.ForeignKey('etudiants.Promotion', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"
    
    def calculer_moyenne(self):
        # À implémenter
        return 0.0
    
    def get_taux_reussite(self):
        # À implémenter
        return 0.0

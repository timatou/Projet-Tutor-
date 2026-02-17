from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Note(models.Model):
    TYPE_CHOICES = [
        ('DS', 'Devoir Surveillé'),
        ('TP', 'Travaux Pratiques'),
        ('EXAM', 'Examen Final'),
    ]

    etudiant = models.ForeignKey(
        'etudiants.Etudiant',   
        on_delete=models.CASCADE,
        related_name='notes'
    )
    module = models.ForeignKey(
        'cours.Module',
        on_delete=models.CASCADE,
        related_name='notes'
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    valeur = models.FloatField(
    validators=[MinValueValidator(0.00), MaxValueValidator(20.0)],
    help_text="La note doit être comprise entre 0 et 20")
    date = models.DateField(auto_now_add=True)

    class Meta:
       
        ordering = ['module', 'etudiant']

    def __str__(self):
        return f"{self.etudiant} - {self.module.libelle} ({self.type} : {self.valeur})"


class Absence(models.Model):
    etudiant = models.ForeignKey(
        'etudiants.Etudiant',
        on_delete=models.CASCADE,
        related_name='absences'
    )
    module = models.ForeignKey(
        'cours.Module',
        on_delete=models.CASCADE,
        related_name='absences'
    )
    date = models.DateField()
    duree = models.DecimalField(  
        max_digits=4,  
        decimal_places=2,
        help_text="Durée de l'absence en heures"
    )
    justifiee = models.BooleanField(default=False)
    motif = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        status = "Justifiée" if self.justifiee else "Non justifiée"
        return f"{self.etudiant} - {self.module.libelle} ({self.date}) - {self.duree}h [{status}]"
    
    # Dans la classe Absence
    def est_longue_absence(self):
        return self.duree > 4  # Exemple : alerte si plus de 4h
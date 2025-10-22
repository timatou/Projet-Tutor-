from django.db import models


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
    valeur = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.etudiant.prenom} {self.etudiant.nom} - {self.module.libelle} ({self.type} : {self.valeur})"

    class Meta:
        unique_together = ('etudiant', 'module', 'type')
        ordering = ['module', 'etudiant']
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
    justifiee = models.BooleanField(default=False)
    motif = models.TextField(blank=True, null=True)

    def __str__(self):
        status = "Justifiée" if self.justifiee else "Non justifiée"
        return f"{self.etudiant.prenom} {self.etudiant.nom} - {self.module.libelle} ({self.date}) [{status}]"

    class Meta:
        ordering = ['-date']
        verbose_name = "Absence"
        verbose_name_plural = "Absences"

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Max, Min


# ==========================================
#               EPREUVE
# ==========================================

class Epreuve(models.Model):

    TYPE_CHOICES = [
        ('DS', 'Devoir Surveillé'),
        ('TP', 'Travaux Pratiques'),
        ('EXAM', 'Examen Final'),
    ]

    module = models.ForeignKey(
        'cours.Module',
        on_delete=models.CASCADE,
        related_name='epreuves'
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    date = models.DateField()

    coefficient = models.FloatField(
        default=1,
        validators=[MinValueValidator(0.1)],
        help_text="Coefficient de l'épreuve"
    )

    class Meta:
        unique_together = ('module', 'type', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.module.libelle} - {self.type} ({self.date})"

    # Moyenne de l'épreuve
    def moyenne(self):
        return self.notes.aggregate(Avg('valeur'))['valeur__avg']

    # Note maximale
    def note_max(self):
        return self.notes.aggregate(Max('valeur'))['valeur__max']

    # Note minimale
    def note_min(self):
        return self.notes.aggregate(Min('valeur'))['valeur__min']


# ==========================================
#                 NOTE
# ==========================================

class Note(models.Model):

    etudiant = models.ForeignKey(
        'etudiants.Etudiant',
        on_delete=models.CASCADE,
        related_name='notes'
    )

    epreuve = models.ForeignKey(
        'Epreuve',
        on_delete=models.CASCADE,
        related_name='notes'
    )

    valeur = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(20.0)
        ],
        help_text="La note doit être comprise entre 0 et 20"
    )

    class Meta:
        unique_together = ('etudiant', 'epreuve')
        ordering = ['epreuve']

    def __str__(self):
        return f"{self.etudiant} - {self.epreuve} : {self.valeur}"

    def est_reussie(self):
        return self.valeur >= 10


# ==========================================
#               ABSENCE
# ==========================================

class Absence(models.Model):

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('REFUSEE', 'Refusée'),
    ]

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

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )

    motif = models.TextField(
        blank=True,
        null=True
    )

    justificatif = models.FileField(
        upload_to='justificatifs/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.etudiant} - {self.module.libelle} ({self.date}) - {self.duree}h [{self.statut}]"

    def est_longue_absence(self):
        return self.duree > 4
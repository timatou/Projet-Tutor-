from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('PROFESSEUR', 'Professeur'),
        ('ETUDIANT', 'Etudiant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ETUDIANT')

    @property 
    def is_professeur(self):
        return self.role == 'PROFESSEUR'

    @property
    def is_admin(self):
        return self.role == 'ADMIN' 
    
    @property
    def is_etudiant(self):
        return self.role == 'ETUDIANT' 

    def __str__(self):
        return f"{self.username} ({self.role})"


class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    departement = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Admin {self.user.get_full_name()}"


class Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professeur_profile')
    specialite = models.CharField(max_length=100, blank=True)

    def __str__(self):
        nom_complet = self.user.get_full_name()
        if not nom_complet.strip():
            nom_complet = self.user.username
        return f"{nom_complet} ({self.specialite})"


class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etudiant_profile')
    promotion = models.CharField(max_length=50)
    groupe = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.promotion}"
    
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Professeur)
@receiver(post_save, sender=Administrateur)
@receiver(post_save, sender=Etudiant)
def update_user_role(sender, instance, created, **kwargs):
    if created:
        if sender == Professeur:
            instance.user.role = 'PROFESSEUR'
        elif sender == Administrateur:
            instance.user.role = 'ADMIN'
        elif sender == Etudiant:
            instance.user.role = 'ETUDIANT'
        instance.user.save()
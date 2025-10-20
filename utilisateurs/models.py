from django.db import models

# Create your models here.
# utilisateurs/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('PROFESSEUR', 'Professeur'),
        ('ADMIN', 'Administrateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PROFESSEUR')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professeur_profile')
    specialite = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Prof. {self.user.first_name} {self.user.last_name}"

class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    departement = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Admin. {self.user.first_name} {self.user.last_name}"
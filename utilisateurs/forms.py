from django import forms
from .models import User, Professeur
from cours.models import Module

class ProfesseurRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Identifiant")
    first_name = forms.CharField(max_length=150, label="Prénom")
    last_name = forms.CharField(max_length=150, label="Nom")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")

    class Meta:
        model = Professeur
        fields = ['specialite']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role='PROFESSEUR'
        )
        professeur = super().save(commit=False)
        professeur.user = user
        if commit:
            professeur.save()
        return professeur

class ProfesseurUpdateForm(forms.ModelForm):
    # On définit les modules pour qu'ils apparaissent dans le formulaire
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Modules enseignés"
    )

    class Meta:
        model = Professeur
        fields = ['specialite'] # On peut modifier la spécialité aussi

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-cocher les modules que le prof possède déjà
        if self.instance and self.instance.pk:
            self.fields['modules'].initial = self.instance.modules.all()

    def save(self, commit=True):
        # Sauvegarde du modèle Professeur (spécialité)
        professeur = super().save(commit=commit)
        if commit:
            # Sauvegarde de la relation Many-to-Many avec les modules
            # C'est cette ligne précise qui met à jour tes cases cochées
            self.instance.modules.set(self.cleaned_data['modules'])
        return professeur
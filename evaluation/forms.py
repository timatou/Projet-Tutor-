from django import forms
from .models import Note
from .models import Absence

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['etudiant', 'epreuve', 'valeur']

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['etudiant', 'module', 'date', 'duree', 'justifiee', 'motif']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
        }
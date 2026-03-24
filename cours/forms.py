from django import forms
from .models import Module
from etudiants.models import Promotion

class ModuleUpdateForm(forms.ModelForm):
    promotions = forms.ModelMultipleChoiceField(
        queryset=Promotion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Promotions assignées"
    )

    class Meta:
        model = Module
        fields = ['code', 'libelle', 'coefficient', 'semestre', 'promotions']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control'}),
        }
from django.db import models


class Statistique:

    @staticmethod
    def moyenne_par_module(module):
        from evaluation.models import Note
        notes = Note.objects.filter(module=module)
        if not notes.exists():
            return 0
        return round(sum(note.valeur for note in notes) / len(notes), 2)

    @staticmethod
    def moyenne_par_etudiant(etudiant):
        from evaluation.models import Note
        notes = Note.objects.filter(etudiant=etudiant)
        if not notes.exists():
            return 0
        return round(sum(note.valeur for note in notes) / len(notes), 2)

    @staticmethod
    def taux_absence_etudiant(etudiant):
        from evaluation.models import Absence
        total = Absence.objects.filter(etudiant=etudiant).count()
        justifiees = Absence.objects.filter(etudiant=etudiant, justifiee=True).count()
        if total == 0:
            return 0
        return round((total - justifiees) / total * 100, 2)
    
    @staticmethod
    def evolution_notes_etudiant(etudiant):
        from evaluation.models import Note
        # Récupère les notes triées par date
        notes = Note.objects.filter(etudiant=etudiant).order_by('date')
        return {
            "labels": [note.date.strftime("%d/%m") for note in notes],
            "data": [note.valeur for note in notes]
    }

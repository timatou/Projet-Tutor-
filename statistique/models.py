from django.db.models import Avg, Count, Q

class Statistique:
    @staticmethod
    def moyenne_par_module(module):
        from evaluation.models import Note
        res = Note.objects.filter(module=module).aggregate(Avg('valeur'))
        return round(res['valeur__avg'] or 0, 2)

    @staticmethod
    def moyenne_par_etudiant(etudiant):
        from evaluation.models import Note
        res = Note.objects.filter(etudiant=etudiant).aggregate(Avg('valeur'))
        return round(res['valeur__avg'] or 0, 2)

    @staticmethod
    def taux_absence_etudiant(etudiant):
        from evaluation.models import Absence
        stats = Absence.objects.filter(etudiant=etudiant).aggregate(
            total=Count('id'),
            justifiees=Count('id', filter=Q(justifiee=True))
        )
        if stats['total'] == 0: return 0
        injustifiees = stats['total'] - stats['justifiees']
        return round((injustifiees / stats['total']) * 100, 2)
    
    @staticmethod
    def evolution_notes_etudiant(etudiant):
        from evaluation.models import Note
        notes = Note.objects.filter(etudiant=etudiant).order_by('date')
        return {
            "labels": [n.date.strftime("%d/%m") for n in notes],
            "data": [n.valeur for n in notes]
        }
    
    # Dans ta classe Statistique (models.py)
@staticmethod
def notes_par_module_etudiant(etudiant):
    from evaluation.models import Note
    # On récupère la dernière note de l'étudiant pour chaque module
    notes = Note.objects.filter(etudiant=etudiant)
    return {
        "labels": [n.module.libelle for n in notes],
        "data": [n.valeur for n in notes]
    }
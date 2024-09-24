from django.db import models
import uuid
from datetime import date

class Pays(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.pays


class Etablissement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255, blank=True, null=True)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='etablissements', blank=True, null=True)

    def __str__(self):
        return self.nom


class Doctorant(models.Model):
    DOCTORAT_CHOICES = [
        ('LMD', 'LMD (5 years)'),
        ('Classique', 'Classique (6 years)')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True)
    fonction = models.CharField(max_length=255, blank=True, null=True)
    emails = models.JSONField(default=list, blank=True, null=True)
    telephones = models.JSONField(default=list, blank=True, null=True)
    etablissement_origine_graduation = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='doctorants_graduation', blank=True, null=True)
    etablissement_origine_magister = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='doctorants_magister', blank=True, null=True)
    etablissement_origine = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='doctorants_origine', blank=True, null=True)
    etablissement_exercice = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='doctorants_exercice', blank=True, null=True)
    type_doctorat = models.CharField(max_length=50, choices=DOCTORAT_CHOICES)
    premiere_inscription = models.DateField(blank=True, null=True)
    titre_these = models.TextField(blank=True, null=True)
    date_enregistrement_these = models.DateField(blank=True, null=True)
    laboratoire = models.CharField(max_length=255, blank=True, null=True, choices=[('LCSI', 'LCSI'), ('LMCS', 'LMCS'), ('Externe', 'Externe')])
    directeur_these = models.ForeignKey('Expert', on_delete=models.CASCADE, related_name='doctorants_directeurs', blank=True, null=True)
    co_directeur_these = models.ForeignKey('Expert', on_delete=models.CASCADE, related_name='doctorants_co_directeurs', blank=True, null=True)
    situation = models.CharField(max_length=255, blank=True, null=True)
    date_soutenance_pv_abandon = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    @property
    def nombre_reinscriptions(self):
        """Calculate the number of re-inscriptions based on the PV entries."""
        return self.pvs.filter(annee__gte=self.premiere_inscription.year).count()

    @property
    def retardataire(self):
        """Determine if the student is delayed."""
        duration = 5 if self.type_doctorat == 'LMD' else 6
        years_spent = date.today().year - self.premiere_inscription.year
        return self.nombre_reinscriptions > duration or years_spent > duration


class Expert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    grade = models.CharField(max_length=50, choices=[('MCA', 'MCA'), ('PR', 'PR')])
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='experts_etablissement', blank=True, null=True)
    emails = models.JSONField(default=list, blank=True, null=True)
    telephones = models.JSONField(default=list, blank=True, null=True)
    nombre_evaluations = models.IntegerField(default=0)
    nombre_publications = models.IntegerField(default=0)
    mots_cles = models.ManyToManyField('MotCle', related_name='experts', blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class PV(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='pvs')
    annee = models.IntegerField()
    pv_document = models.TextField()

    def __str__(self):
        return f"PV {self.id} - {self.doctorant.nom} {self.doctorant.prenom}"


class Publication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.TextField()
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='publications')
    source = models.CharField(max_length=50, choices=[('Google Scholar', 'Google Scholar'), ('ResearchGate', 'ResearchGate'), ('DBLP', 'DBLP'), ('Autre', 'Autre')])

    def __str__(self):
        return self.titre


class Evaluation(models.Model):
    EVALUATION_DECISION_CHOICES = [
        ('Favorable', 'Favorable'),
        ('Favorable sous réserve', 'Favorable sous réserve'),
        ('Défavorable', 'Défavorable')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='evaluations')
    expert_1 = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='evaluations_as_expert_1')
    expert_2 = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='evaluations_as_expert_2')
    type_evaluation = models.CharField(max_length=50, choices=[('Réinscription', 'Réinscription'), ('Soutenance', 'Soutenance')])
    avis_expert_1 = models.CharField(max_length=50, choices=EVALUATION_DECISION_CHOICES)
    avis_expert_2 = models.CharField(max_length=50, choices=EVALUATION_DECISION_CHOICES)
    commentaire_expert_1 = models.TextField(blank=True, null=True)
    commentaire_expert_2 = models.TextField(blank=True, null=True)
    date_evaluation = models.DateField()

    def __str__(self):
        return f"Evaluation {self.id} - {self.doctorant.nom} {self.doctorant.prenom}"

    @property
    def defavorable(self):
        """Check if either expert gave a 'Défavorable' decision."""
        return self.avis_expert_1 == 'Défavorable' or self.avis_expert_2 == 'Défavorable'


class MotCle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mot_cle = models.CharField(max_length=255)
    source = models.CharField(max_length=50, choices=[('Google Scholar', 'Google Scholar'), ('ResearchGate', 'ResearchGate'), ('DBLP', 'DBLP'), ('Autre', 'Autre')])

    def __str__(self):
        return self.mot_cle



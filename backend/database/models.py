from django.db import models
import uuid

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
    type_doctorat = models.CharField(max_length=255, blank=True, null=True)
    premiere_inscription = models.DateField(blank=True, null=True)
    titre_these = models.TextField(blank=True, null=True)
    date_enregistrement_these = models.DateField(blank=True, null=True)
    laboratoire = models.CharField(max_length=255, blank=True, null=True)
    directeur_these = models.ForeignKey('Expert', on_delete=models.CASCADE, related_name='doctorants_directeurs', blank=True, null=True)
    co_directeur_these = models.ForeignKey('Expert', on_delete=models.CASCADE, related_name='doctorants_co_directeurs', blank=True, null=True)
    situation = models.CharField(max_length=255, blank=True, null=True)
    date_soutenance_pv_abandon = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='evaluations')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='evaluations')
    decision_attribution = models.TextField()
    date_attribution = models.DateField()

    def __str__(self):
        return f"Evaluation {self.id} - {self.doctorant.nom} {self.doctorant.prenom} - {self.expert.nom} {self.expert.prenom}"


class MotCle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mot_cle = models.CharField(max_length=255)
    source = models.CharField(max_length=50, choices=[('Google Scholar', 'Google Scholar'), ('ResearchGate', 'ResearchGate'), ('DBLP', 'DBLP'), ('Autre', 'Autre')])

    def __str__(self):
        return self.mot_cle



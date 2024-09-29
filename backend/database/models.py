from django.db import models
import uuid
from datetime import date
from django.db.models import Count, Q


class Pays(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.pays


class Etablissement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255, blank=True, null=True)
    pays = models.ForeignKey(
        Pays,
        on_delete=models.CASCADE,
        related_name="etablissements",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nom


class Laboratoire(models.Model):
    """Modèle pour représenter les laboratoires auxquels les doctorants peuvent appartenir."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Doctorant(models.Model):
    DOCTORAT_CHOICES = [("LMD", "LMD (5 years)"), ("Classique", "Classique (6 years)")]
    SITUATION_CHOICES = [
        ("Inscrit", "Inscrit"),
        ("Soutenu", "Soutenu"),
        ("Abandon", "Abandon"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True)
    fonction = models.CharField(max_length=255, blank=True, null=True)
    emails = models.JSONField(default=list, blank=True, null=True)
    telephones = models.JSONField(default=list, blank=True, null=True)
    etablissement_origine_graduation = models.ForeignKey(
        "Etablissement",
        on_delete=models.CASCADE,
        related_name="doctorants_graduation",
        blank=True,
        null=True,
    )
    etablissement_origine_magister = models.ForeignKey(
        "Etablissement",
        on_delete=models.CASCADE,
        related_name="doctorants_magister",
        blank=True,
        null=True,
    )
    etablissement_origine = models.ForeignKey(
        "Etablissement",
        on_delete=models.CASCADE,
        related_name="doctorants_origine",
        blank=True,
        null=True,
    )
    etablissement_exercice = models.ForeignKey(
        "Etablissement",
        on_delete=models.CASCADE,
        related_name="doctorants_exercice",
        blank=True,
        null=True,
    )
    type_doctorat = models.CharField(max_length=50, choices=DOCTORAT_CHOICES)
    premiere_inscription = models.DateField(blank=True, null=True)
    titre_these = models.TextField(blank=True, null=True)
    date_enregistrement_these = models.DateField(blank=True, null=True)
    specialite = models.CharField(max_length=100, blank=True, null=True)
    laboratoires = models.ManyToManyField(
        "Laboratoire", related_name="doctorants", blank=True
    )
    situation = models.CharField(
        max_length=50, choices=SITUATION_CHOICES, default="Inscrit", blank=False
    )
    directeur_these = models.ForeignKey(
        "Expert",
        on_delete=models.CASCADE,
        related_name="doctorants_directeurs",
        blank=True,
        null=True,
    )
    co_directeur_these = models.ForeignKey(
        "Expert",
        on_delete=models.CASCADE,
        related_name="doctorants_co_directeurs",
        blank=True,
        null=True,
    )
    date_soutenance_pv_abandon = models.DateField(blank=True, null=True)
    annee_etude = models.IntegerField(default=1)  # Ajout du champ année d'étude

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    @property
    def retardataire(self):
        """Détermine si le doctorant est retardataire."""
        duration = 5 if self.type_doctorat == "LMD" else 6
        return self.annee_etude > duration

    @staticmethod
    def obtenir_retardataires():
        return [
            doctorant for doctorant in Doctorant.objects.all() if doctorant.retardataire
        ]

    @staticmethod
    def statistiques_par_annee():
        stats = Doctorant.objects.values(
            "situation", "premiere_inscription__year"
        ).annotate(total=models.Count("id"))
        return stats

    @staticmethod
    def statistiques_par_sexe():
        stats = Doctorant.objects.filter(situation='Inscrit').values('sexe', 'premiere_inscription__year').annotate(total=models.Count('id'))
        return stats

    @staticmethod
    def statistiques_par_specialite():
        stats = Doctorant.objects.filter(situation='Inscrit').values('specialite', 'premiere_inscription__year').annotate(
            total=models.Count("id")
        )
        return stats

    @staticmethod
    def statistiques_par_type():
        stats = Doctorant.objects.filter(situation='Inscrit').values('type_doctorat', 'premiere_inscription__year').annotate(
            total=models.Count("id")
        )
        return stats

    @staticmethod
    def statistiques_par_annee_et_statut_evaluation():
        # Compter le nombre d'admis et non admis par année
        stats = (
            Doctorant.objects.values("premiere_inscription__year")
            .annotate(
                admis=Count("evaluations", filter=Q(evaluations__statut="admis")),
                non_admis=Count(
                    "evaluations", filter=Q(evaluations__statut="non admis")
                ),
            )
            .order_by("premiere_inscription__year")  # Tri par année
        )
        return stats

    @staticmethod
    def statistiques_par_laboratoire():
        stats = (
            Doctorant.objects.filter(situation="Inscrit")
            .values("laboratoires__nom", "premiere_inscription__year")
            .annotate(total=models.Count("id"))
            .order_by("laboratoires__nom", "premiere_inscription__year")
        )
        return stats
    def statistiques_par_annee_etude():
        return (
            Doctorant.objects.filter(situation='Inscrit').values("annee_etude", "premiere_inscription__year")
            .annotate(total=Count("id"))
            .order_by("annee_etude")
        )


class Expert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    grade = models.CharField(max_length=50, choices=[("MCA", "MCA"), ("PR", "PR")])
    etablissement = models.ForeignKey(
        Etablissement,
        on_delete=models.CASCADE,
        related_name="experts_etablissement",
        blank=True,
        null=True,
    )
    emails = models.JSONField(default=list, blank=True, null=True)
    telephones = models.JSONField(default=list, blank=True, null=True)
    nombre_expertises = models.IntegerField(default=0)
    nombre_publications = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class PV(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorant = models.ForeignKey(
        Doctorant, on_delete=models.CASCADE, related_name="pvs"
    )
    annee = models.IntegerField()
    pv_document = models.TextField()

    def __str__(self):
        return f"PV {self.id} - {self.doctorant.nom} {self.doctorant.prenom}"


class Expertise(models.Model):
    EXPERTISE_DECISION_CHOICES = [
        ("Favorable", "Favorable"),
        ("Favorable sous réserve", "Favorable sous réserve"),
        ("Défavorable", "Défavorable"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorant = models.ForeignKey(
        Doctorant, on_delete=models.CASCADE, related_name="expertises"
    )
    expert_1 = models.ForeignKey(
        Expert, on_delete=models.CASCADE, related_name="expertises_as_expert_1"
    )
    expert_2 = models.ForeignKey(
        Expert, on_delete=models.CASCADE, related_name="expertises_as_expert_2"
    )
    expert_3 = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        related_name="expertises_as_expert_3",
        blank=True,
        null=True,
    )
    avis_expert_1 = models.CharField(max_length=50, choices=EXPERTISE_DECISION_CHOICES)
    avis_expert_2 = models.CharField(max_length=50, choices=EXPERTISE_DECISION_CHOICES)
    avis_expert_3 = models.CharField(
        max_length=50, choices=EXPERTISE_DECISION_CHOICES, blank=True, null=True
    )
    commentaire_expert_1 = models.TextField(blank=True, null=True)
    commentaire_expert_2 = models.TextField(blank=True, null=True)
    commentaire_expert_3 = models.TextField(blank=True, null=True)
    date_expertise = models.DateField()

    def __str__(self):
        return f"Expertise {self.id} - {self.doctorant.nom} {self.doctorant.prenom}"

    @property
    def defavorable(self):
        return (
            self.avis_expert_1 == "Défavorable" or self.avis_expert_2 == "Défavorable"
        )

    @property
    def necessite_expert_3(self):
        return self.defavorable and self.expert_3 is None


class MotCle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mot_cle = models.CharField(max_length=255)
    source = models.CharField(
        max_length=50,
        choices=[
            ("Google Scholar", "Google Scholar"),
            ("ResearchGate", "ResearchGate"),
            ("DBLP", "DBLP"),
            ("Autre", "Autre"),
        ],
    )

    def __str__(self):
        return self.mot_cle


class Publication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.TextField()
    expert = models.ForeignKey(
        Expert, on_delete=models.CASCADE, related_name="publications"
    )
    source = models.CharField(
        max_length=50,
        choices=[
            ("Google Scholar", "Google Scholar"),
            ("ResearchGate", "ResearchGate"),
            ("DBLP", "DBLP"),
            ("Autre", "Autre"),
        ],
    )

    def __str__(self):
        return self.titre


class Evaluation(models.Model):
    EVALUATION_STATUT_CHOICES = [("Admis", "Admis"), ("Non admis", "Non admis")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorant = models.ForeignKey(
        "Doctorant", on_delete=models.CASCADE, related_name="evaluations"
    )
    date_evaluation = models.DateField()  # Date de l'évaluation (octobre, mars)
    statut = models.CharField(
        max_length=50, choices=EVALUATION_STATUT_CHOICES, default="Non admis"
    )
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Évaluation {self.id} - {self.doctorant.nom} {self.doctorant.prenom}"

    @property
    def deuxieme_evaluation(self):
        """Détermine si une deuxième évaluation est nécessaire (mars)."""
        return self.statut == "Non admis"

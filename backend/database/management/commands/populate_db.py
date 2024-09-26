from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from database.models import Pays, Evaluation, Etablissement, Laboratoire, Expert, Doctorant, PV, Expertise

class Command(BaseCommand):
    help = 'Populate the database with test data.'

    def handle(self, *args, **kwargs):
        # Create countries
        pays_list = ["Algeria", "France", "Germany", "USA"]
        pays_instances = [Pays.objects.create(pays=p) for p in pays_list]

        # Create institutions
        etablissements = [
            Etablissement.objects.create(
                nom=f"Etablissement {i}",
                ville=f"Ville {i}",
                pays=random.choice(pays_instances)
            )
            for i in range(10)
        ]

        # Create laboratories
        laboratoires = [
            Laboratoire.objects.create(
                nom=i,
                description=f"Description for lab {i}"
            )
            for i in ['LMCS', 'LCSI', 'Autre']
        ]

        # Create experts
        experts = [
            Expert.objects.create(
                nom=f"Nom Expert {i}",
                prenom=f"Prenom Expert {i}",
                grade=random.choice(['MCA', 'PR']),
                etablissement=random.choice(etablissements),
                emails=[f"expert{i}@example.com"],
                telephones=[f"0123456789{i}"],
                nombre_expertises=random.randint(0, 50),
                nombre_publications=random.randint(0, 100),
            )
            for i in range(20)
        ]

        # Create doctorants
        doctorants = []
        for i in range(50):
            doctorant = Doctorant.objects.create(
                nom=f"Nom Doctorant {i}",
                prenom=f"Prenom Doctorant {i}",
                date_naissance=timezone.now() - timedelta(days=random.randint(8000, 10000)),
                sexe=random.choice(['M', 'F']),
                fonction=f"Fonction {i}",
                emails=[f"doctorant{i}@example.com"],
                telephones=[f"0123456789{i}"],
                etablissement_origine_graduation=random.choice(etablissements),
                etablissement_origine_magister=random.choice(etablissements),
                etablissement_exercice=random.choice(etablissements),
                type_doctorat=random.choice(['LMD', 'Classique']),
                premiere_inscription=timezone.now() - timedelta(days=random.randint(1000, 2000)),
                titre_these=f"Titre de these {i}",
                date_enregistrement_these=timezone.now() - timedelta(days=random.randint(500, 1000)),
                specialite=random.choice(['SIQ', 'SI', 'IA']),
                situation=random.choice(['Inscrit', 'Soutenu', 'Abandon']),
                annee_etude=random.randint(1, 8)
            )
            doctorant.laboratoires.set(random.sample(laboratoires, random.randint(1, 2)))
            doctorant.directeur_these = random.choice(experts)
            doctorant.co_directeur_these = random.choice(experts)
            doctorant.save()
            doctorants.append(doctorant)

            # Create evaluations for each doctorant
            evaluations = [
                Evaluation(
                    doctorant=doctorant,
                    statut=random.choice(['Admis', 'Non Admis']),
                    date_evaluation=timezone.now() - timedelta(days=random.randint(1, 1000)),
                )
                for _ in range(random.randint(1, 3))  # Random number of evaluations
            ]
            Evaluation.objects.bulk_create(evaluations)

        # Create PVs for each doctorant
        pvs = [
            PV(
                doctorant=doctorant,
                annee=year,
                pv_document=f"PV document for {doctorant.nom} {doctorant.prenom}, year {year}"
            )
            for doctorant in doctorants
            for year in range(doctorant.premiere_inscription.year, timezone.now().year + 1)
        ]
        PV.objects.bulk_create(pvs)

        # Create expertises for each doctorant
        expertises = [
            Expertise(
                doctorant=doctorant,
                expert_1=random.choice(experts),
                expert_2=random.choice(experts),
                avis_expert_1=random.choice(['Favorable', 'Défavorable', 'Favorable sous réserve']),
                avis_expert_2=random.choice(['Favorable', 'Défavorable', 'Favorable sous réserve']),
                date_expertise=timezone.now() - timedelta(days=random.randint(100, 500)),
            )
            for doctorant in doctorants
        ]
        Expertise.objects.bulk_create(expertises)

        # Return a success message
        self.stdout.write(self.style.SUCCESS('Database populated with test data successfully'))

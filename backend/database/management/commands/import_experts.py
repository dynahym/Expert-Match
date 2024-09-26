import pandas as pd
from django.core.management.base import BaseCommand
from database.models import Pays, Etablissement, Expert, Publication, MotCle
from backend.fetch import fetch_researcher_data

class Command(BaseCommand):
    help = 'Import experts from an Excel file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            data = pd.read_excel(file_path)
            for _, row in data.iterrows():
                etablissement_name = row.get('etablissement', '').strip()
                ville = row.get('ville', '').strip()
                pays_name = row.get('pays', '').strip()

                pays = self.get_or_create_pays(pays_name)
                etablissement = self.get_or_create_etablissement(etablissement_name, ville, pays)

                expert_name = row.get('nom', '').strip()
                expert_prenom = row.get('prenom', '').strip()

                publications, interests = fetch_researcher_data(expert_prenom, expert_name)
                mot_cle_list = self.get_create_interests(interests)
                expert = self.create_or_update_expert(row, expert_name, expert_prenom, etablissement, publications)

                expert.mots_cles.set(mot_cle_list)
                self.add_publications(expert, publications)

            self.stdout.write(self.style.SUCCESS('Experts imported successfully'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('File not found'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(str(e)))

    def get_or_create_pays(self, pays_name):
        pays, _ = Pays.objects.get_or_create(pays=pays_name)
        return pays

    def get_or_create_etablissement(self, etablissement_name, ville, pays):
        etablissement, _ = Etablissement.objects.get_or_create(
            nom=etablissement_name,
            ville=ville,
            pays=pays
        )
        return etablissement

    def get_create_interests(self, interests):
        mot_cle_list = []
        for interest, source in interests:
            if interest.strip():
                mot_cle, _ = MotCle.objects.update_or_create(
                    mot_cle=interest,
                    defaults={'source': source}
                )
                mot_cle_list.append(mot_cle)
        return mot_cle_list

    def create_or_update_expert(self, row, expert_name, expert_prenom, etablissement, publications):
        expert, _ = Expert.objects.update_or_create(
            nom=expert_name,
            prenom=expert_prenom,
            defaults={
                'etablissement': etablissement,
                'emails': row.get('emails', '').split(';') if pd.notna(row.get('emails', '')) else [],
                'telephones': row.get('telephones', '').split(';') if pd.notna(row.get('telephones', '')) else [],
                'nombre_evaluations': 0,
                'nombre_publications': len(publications),
                'grade': row.get('grade', '').strip(),
            }
        )
        return expert

    def add_publications(self, expert, publications):
        for title, source in publications:
            Publication.objects.update_or_create(
                titre=title,
                expert=expert,
                defaults={'source': source}
            )

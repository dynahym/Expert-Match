import pandas as pd
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pays, Etablissement, Doctorant, Expert, PV, Publication, Evaluation, MotCle
from .serializers import (
    PaysSerializer, EtablissementSerializer, DoctorantSerializer, ExpertSerializer, PVSerializer, 
    PublicationSerializer, EvaluationSerializer, MotCleSerializer, FilePathSerializer
)
from backend.fetch import fetch_researcher_data

class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer

class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer

class DoctorantViewSet(viewsets.ModelViewSet):
    queryset = Doctorant.objects.all()
    serializer_class = DoctorantSerializer

class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class PVViewSet(viewsets.ModelViewSet):
    queryset = PV.objects.all()
    serializer_class = PVSerializer

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

class MotCleViewSet(viewsets.ModelViewSet):
    queryset = MotCle.objects.all()
    serializer_class = MotCleSerializer

class ImportExpertsAPIView(APIView):
    def post(self, request):
        serializer = FilePathSerializer(data=request.data)
        
        if serializer.is_valid():
            file_path = serializer.validated_data['file_path']

            try:
                data = pd.read_excel(file_path)
                for _, row in data.iterrows():
                    etablissement_name = row.get('etablissement', '').strip()
                    ville = row.get('ville', '').strip()
                    pays_name = row.get('pays', '').strip()

                    # Ensure 'pays' exists or is created
                    pays = self.get_or_create_pays(pays_name)

                    # Create or update Etablissement
                    etablissement = self.get_or_create_etablissement(etablissement_name, ville, pays)

                    expert_name = row.get('nom', '').strip()
                    expert_prenom = row.get('prenom', '').strip()

                    # Fetch publications and interests
                    publications, interests = fetch_researcher_data(expert_prenom, expert_name)

                    # If interests are less than 4, classify the articles and get top 5 interests
                    # if len(interests) < 4:
                    #     # Assuming articles are just the titles from publications
                    #     articles = [title for title, _ in publications]
                    #     classified_interests = classify_texts(articles, top_s=8, top_t=5)
                    #     interests.extend([(interest, 'Classified') for interest in classified_interests])

                    mot_cle_list = self.get_create_interests(interests)
                    expert = self.create_or_update_expert(row, expert_name, expert_prenom, etablissement, publications)

                    # Associate keywords and publications with the expert
                    expert.mots_cles.set(mot_cle_list)
                    self.add_publications(expert, publications)

                return Response({"message": "Experts imported successfully"}, status=status.HTTP_201_CREATED)

            except FileNotFoundError:
                return Response({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        expert, created = Expert.objects.update_or_create(
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

from rest_framework import viewsets
from .models import Pays, Etablissement, Doctorant, Expert, PV, Publication, Evaluation, MotCle, Expertise, Laboratoire
from .serializers import (
    PaysSerializer, EtablissementSerializer, DoctorantSerializer, ExpertSerializer, PVSerializer,
    PublicationSerializer, EvaluationSerializer, MotCleSerializer, ExpertiseSerializer, LaboratoireSerializer,
)


class ExpertiseViewSet(viewsets.ModelViewSet):
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer


class LaboratoireViewSet(viewsets.ModelViewSet):
    queryset = Laboratoire.objects.all()
    serializer_class = LaboratoireSerializer


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

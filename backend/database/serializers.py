from rest_framework import serializers
from .models import Pays, Etablissement, Doctorant, Expert, PV, Publication, Evaluation, MotCle, Expertise, Laboratoire

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'

class DoctorantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctorant
        fields = '__all__'

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'

class PVSerializer(serializers.ModelSerializer):
    class Meta:
        model = PV
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class MotCleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotCle
        fields = '__all__'
        
class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'
        
class LaboratoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratoire
        fields = '__all__'

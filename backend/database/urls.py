from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    PaysViewSet, EtablissementViewSet, DoctorantViewSet, ExpertViewSet, PVViewSet,
    PublicationViewSet, EvaluationViewSet, MotCleViewSet, ExpertiseViewSet, LaboratoireViewSet
)

router = DefaultRouter()
router.register(r'pays', PaysViewSet)
router.register(r'etablissements', EtablissementViewSet)
router.register(r'doctorants', DoctorantViewSet)
router.register(r'experts', ExpertViewSet)
router.register(r'pvs', PVViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'mots_cles', MotCleViewSet)
router.register(r'expertise', ExpertiseViewSet)
router.register(r'laboratoire', LaboratoireViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

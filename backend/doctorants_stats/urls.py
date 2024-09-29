from django.urls import path
from .views import (
    statistics_year_view, statistics_situation_year_view, statistics_sexe_view, statistics_sexe_year_view,
    statistics_specialite_view, statistics_specialite_year_view, statistics_type_view, statistics_type_year_view,
    statistics_laboratoire_view, statistics_laboratoire_year_view, statistics_annee_etude_view, 
    statistics_annee_etude_year_view, retardataires_view, statistics_evaluation_view
)

urlpatterns = [
    path('annee/', statistics_year_view, name='statistiques_par_year'),
    path('annee/<int:year>/', statistics_situation_year_view, name='statistiques_par_situation_year'),
    path('sexe/', statistics_sexe_view, name='statistiques_par_sexe'),
    path('sexe/<int:year>/', statistics_sexe_year_view, name='statistiques_par_sexe_year'),
    path('specialite/', statistics_specialite_view, name='statistiques_par_specialite'),
    path('specialite/<int:year>/', statistics_specialite_year_view, name='statistiques_par_specialite_year'),
    path('type/', statistics_type_view, name='statistiques_par_type'),
    path('type/<int:year>/', statistics_type_year_view, name='statistiques_par_type_year'),
    path('labo/', statistics_laboratoire_view, name='statistiques_par_laboratoire'),
    path('labo/<int:year>/', statistics_laboratoire_year_view, name='statistiques_par_laboratoire_year'),
    path('annee_etude/', statistics_annee_etude_view, name='statistiques_par_year_etude'),
    path('annee_etude/<int:year>/', statistics_annee_etude_year_view, name='statistiques_par_annee_etude_year'),
    path('retard/', retardataires_view, name='retardataires'),
    path('evaluation/<int:year>/', statistics_evaluation_view, name='statistiques_par_evaluation'),
]
from django.urls import path
from .views import (
    statistics_year_view, statistics_situation_year_view, statistics_sexe_view, statistics_sexe_year_view,
    statistics_specialite_view, statistics_specialite_year_view
)

urlpatterns = [
    path('annee/', statistics_year_view, name='statistiques_par_annee'),
    path('annee/<int:year>/', statistics_situation_year_view, name='statistiques_par_situation_annee'),
    path('sexe/', statistics_sexe_view, name='statistiques_par_sexe'),
    path('sexe/<int:year>/', statistics_sexe_year_view, name='statistiques_par_sexe_annee'),
    path('specialite/', statistics_specialite_view, name='statistiques_par_specialite'),
    path('specialite/<int:year>/', statistics_specialite_year_view, name='statistiques_par_specialite_annee')
]
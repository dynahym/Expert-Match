import os
from django.shortcuts import render
from django.http import HttpResponse
from database.models import Doctorant
from .utils import (
    save_plot,
    plot_stats_year,
    plot_stats_situation_year,
    plot_stats_sexe,
    plot_stats_sexe_year,
    plot_stats_specialite,
    plot_stats_specialite_year,
)


def statistics_year_view(request):
    try:
        stats = list(Doctorant.statistiques_par_annee())

        filename_inscrit = "static/plots/stats_inscrit.png"
        filename_abandon = "static/plots/stats_abandon.png"
        filename_soutenu = "static/plots/stats_soutenu.png"

        save_plot(filename_inscrit, plot_stats_year, stats, "Inscrit", "blue")
        save_plot(filename_abandon, plot_stats_year, stats, "Abandon", "red")
        save_plot(filename_abandon, plot_stats_year, stats, "Soutenu", "green")

        images = {
            "inscrit": "plots/stats_inscrit.png",
            "abandon": "plots/stats_abandon.png",
            "soutenu": "plots/stats_soutenu.png",
        }
        return render(request, "statistics_year.html", {"images": images})

    except ValueError as ve:
        return HttpResponse(f"Erreur de valeur : {str(ve)}")
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des statistiques : {str(e)}")


def statistics_situation_year_view(request, year):
    try:
        stats = list(Doctorant.statistiques_par_annee())
        year = int(year)
        filename = "static/plots/statistics_situation_year.png"
        
        save_plot(filename, plot_stats_situation_year, stats, year)
        
        html = "statistics_situation_year.html"
        image = "plots/statistics_situation_year.png"
        return render(request, html, {"image": image, "year": year})

    except ValueError as ve:
        return HttpResponse(f"Erreur de valeur : {str(ve)}")
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des statistiques : {str(e)}")


def statistics_sexe_view(request):
    try:
        stats = list(Doctorant.statistiques_par_sexe())
        filename = "static/plots/stats_sexe.png"
        
        save_plot(filename, plot_stats_sexe, stats)
        
        html = "statistics_sexe.html"
        image = "plots/stats_sexe.png"
        return render(request, html, {"image": image})
        
    except ValueError as ve:
        return HttpResponse(f"Erreur de valeur : {str(ve)}")
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des statistiques : {str(e)}")


def statistics_sexe_year_view(request, year):
    try:
        stats = list(Doctorant.statistiques_par_sexe())
        year = int(year)
        filename = "static/plots/stats_sexe_year.png"
        
        save_plot(filename, plot_stats_sexe_year, stats, year)
        
        image = "plots/stats_sexe_year.png"
        html = "statistics_sexe_year.html"
        return render(request, html, {"image": image, "year": year})

    except ValueError as ve:
        return HttpResponse(f"Erreur de valeur : {str(ve)}")
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des statistiques : {str(e)}")


def statistics_specialite_view(request):
    try:
        stats = list(Doctorant.statistiques_par_specialite())
        filename = "static/plots/stats_specialite.png"
        
        save_plot(filename, plot_stats_specialite, stats)
        
        html = "statistics_specialite.html"
        image = "plots/stats_specialite.png"
        return render(request, html, {"image": image})

    except ValueError as ve:
        return HttpResponse(f"Erreur de valeur : {str(ve)}")
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des statistiques : {str(e)}")


def statistics_specialite_year_view(request, year):
    try:
        stats = list(Doctorant.statistiques_par_specialite())
        year = int(year)
        filename = "static/plots/stats_specialite_year.png"
        
        save_plot(filename, plot_stats_specialite_year, stats, year)
        
        html = "statistics_specialite_year.html"
        image = "plots/stats_specialite_year.png"
        return render(request, html, {"image": image, "year": year})

    except ValueError as ve:
        return HttpResponse(f"Erreur de valeur : {str(ve)}")
    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération des statistiques : {str(e)}")

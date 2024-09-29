
# Documentation de l'application Django : `doctorant_stats`

## Table des matières
1. [Introduction](#introduction)
2. [URLs](#urls)
   - [1.1. Configuration des URLs](#configuration-des-urls)
   - [1.2. Liste des URLs](#liste-des-urls)
3. [Vues](#vues)
   - [2.1. Présentation des vues](#presentation-des-vues)
   - [2.2. Détails des vues](#details-des-vues)
4. [Utilisation](#utilisation)

## Introduction
Ce projet Django vise à fournir des statistiques sur les doctorants, y compris des fonctionnalités supplémentaires telles que la visualisation des doctorants retardataires et l'évaluation des doctorants par année.

## URLs

### 1.1. Configuration des URLs
Les URLs sont définies dans le fichier `doctorant_stats/urls.py`. Elles sont mappées aux vues correspondantes pour générer les statistiques appropriées.

### 1.2. Liste des URLs

| URL                              | Vue                                             | Nom de la route                         |
|----------------------------------|-------------------------------------------------|----------------------------------------|
| `/annee/`                        | `statistics_year_view`                         | `statistiques_par_year`               |
| `/annee/<int:year>/`            | `statistics_situation_year_view`              | `statistiques_par_situation_year`     |
| `/sexe/`                         | `statistics_sexe_view`                         | `statistiques_par_sexe`                |
| `/sexe/<int:year>/`             | `statistics_sexe_year_view`                   | `statistiques_par_sexe_year`          |
| `/specialite/`                  | `statistics_specialite_view`                  | `statistiques_par_specialite`         |
| `/specialite/<int:year>/`       | `statistics_specialite_year_view`             | `statistiques_par_specialite_year`    |
| `/type/`                         | `statistics_type_view`                         | `statistiques_par_type`               |
| `/type/<int:year>/`             | `statistics_type_year_view`                   | `statistiques_par_type_year`          |
| `/labo/`                         | `statistics_laboratoire_view`                 | `statistiques_par_laboratoire`        |
| `/labo/<int:year>/`             | `statistics_laboratoire_year_view`            | `statistiques_par_laboratoire_year`   |
| `/annee_etude/`                 | `statistics_annee_etude_view`                 | `statistiques_par_year_etude`         |
| `/annee_etude/<int:year>/`      | `statistics_annee_etude_year_view`            | `statistiques_par_annee_etude_year`   |
| `/retard/`                       | `retardataires_view`                           | `retardataires`                        |
| `/evaluation/<int:year>/`       | `statistics_evaluation_view`                  | `statistiques_par_evaluation`         |

## Vues

### 2.1. Présentation des vues
Les vues dans le fichier `doctorant_stats/views.py` sont responsables de la récupération des données statistiques et de leur rendu dans des modèles HTML. Chaque vue traite des statistiques d'un aspect spécifique des doctorants, avec l'ajout des statistiques sur les doctorants retardataires et l'évaluation.

### 2.2. Détails des vues

1. **statistics_year_view(request)**
   - **Description** : Génère des statistiques des doctorants par année (inscrits, abandons, soutenues).
   - **URL associée** : `/annee/`
   - **Renvoie** : un modèle HTML avec les graphiques des statistiques.

2. **statistics_situation_year_view(request, year)**
   - **Description** : Génère des statistiques des doctorants pour une année donnée, filtrées par situation.
   - **URL associée** : `/annee/<int:year>/`
   - **Paramètre** : `year` (année pour filtrer les résultats).
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

3. **statistics_sexe_view(request)**
   - **Description** : Génère des statistiques des doctorants par sexe.
   - **URL associée** : `/sexe/`
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

4. **statistics_sexe_year_view(request, year)**
   - **Description** : Génère des statistiques des doctorants par sexe pour une année donnée.
   - **URL associée** : `/sexe/<int:year>/`
   - **Paramètre** : `year`.
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

5. **statistics_specialite_view(request)**
   - **Description** : Génère des statistiques des doctorants par spécialité.
   - **URL associée** : `/specialite/`
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

6. **statistics_specialite_year_view(request, year)**
   - **Description** : Génère des statistiques par spécialité pour une année donnée.
   - **URL associée** : `/specialite/<int:year>/`
   - **Paramètre** : `year`.
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

7. **statistics_type_view(request)**
   - **Description** : Génère des statistiques des doctorants par type.
   - **URL associée** : `/type/`
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

8. **statistics_type_year_view(request, year)**
   - **Description** : Génère des statistiques par type pour une année donnée.
   - **URL associée** : `/type/<int:year>/`
   - **Paramètre** : `year`.
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

9. **statistics_laboratoire_view(request)**
   - **Description** : Génère des statistiques des doctorants par laboratoire.
   - **URL associée** : `/labo/`
   - **Renvoie** : un modèle HTML avec le graphique des statistiques.

10. **statistics_laboratoire_year_view(request, year)**
    - **Description** : Génère des statistiques par laboratoire pour une année donnée.
    - **URL associée** : `/labo/<int:year>/`
    - **Paramètre** : `year`.
    - **Renvoie** : un modèle HTML avec le graphique des statistiques.

11. **statistics_annee_etude_view(request)**
    - **Description** : Génère des statistiques des doctorants par année d'étude.
    - **URL associée** : `/annee_etude/`
    - **Renvoie** : un modèle HTML avec le graphique des statistiques.

12. **statistics_annee_etude_year_view(request, year)**
    - **Description** : Génère des statistiques par année d'étude pour une année donnée.
    - **URL associée** : `/annee_etude/<int:year>/`
    - **Paramètre** : `year`.
    - **Renvoie** : un modèle HTML avec le graphique des statistiques.

13. **retardataires_view(request)**
    - **Description** : Génère des statistiques sur les doctorants retardataires (inscrits après la date limite).
    - **URL associée** : `/retard/`
    - **Renvoie** : un modèle HTML avec les statistiques des doctorants retardataires.

14. **statistics_evaluation_view(request, year)**
    - **Description** : Génère des statistiques d'évaluation des doctorants pour une année donnée.
    - **URL associée** : `/evaluation/<int:year>/`
    - **Paramètre** : `year`.
    - **Renvoie** : un modèle HTML avec les graphiques d'évaluation.

## Utilisation
Pour utiliser ce projet :

1. **Démarrer le serveur Django** :
   Exécutez la commande suivante :
   ```bash
   python manage.py runserver
   ```

2. **Accéder aux statistiques** :
   Ouvrez un navigateur et accédez aux différentes URLs définies pour visualiser les statistiques des doctorants. Par exemple :
   - Pour visualiser les statistiques par année : [http://localhost:8000/annee/](http://localhost:8000/annee/)
   - Pour visualiser les retardataires : [http://localhost:8000/retard/](http://localhost:8000/retard/)
   - Pour évaluer les doctorants pour une année donnée : [http://localhost:8000/evaluation/2023/](http://localhost:8000/evaluation/2023/)
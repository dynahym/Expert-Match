# Documentation de l'application Django : `data_classification`

## Table des matières
1. [Introduction](#introduction)
2. [Modules](#modules)
   - [2.1. fetch.py](#fetchpy)
   - [2.2. classify.py](#classifypy)
   - [2.3. match.py](#matchpy)
3. [Utilisation](#utilisation)

## Introduction
L'application `data_classification` est conçue pour récupérer, classifier et faire correspondre des données de recherche, y compris les articles et les intérêts des chercheurs. Elle utilise des API externes pour collecter des informations et propose des experts basés sur des titres de thèse.

## Modules

### 2.1. `fetch.py`
Ce module est responsable de la récupération des données de recherche à partir de différentes sources.

#### Fonctions

- **`fetch_researcher_data(first_name: str, last_name: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]`**
  - **Description** : Récupère les données des chercheurs (articles, intérêts) à partir de DBLP, Google Scholar et ResearchGate en parallèle.
  - **Arguments** :
    - `first_name` (str) : Le prénom du chercheur.
    - `last_name` (str) : Le nom de famille du chercheur.
  - **Retourne** : Un tuple contenant deux listes :
    - Une liste d'articles uniques (titres de chaînes) avec leurs sources.
    - Une liste d'intérêts de recherche uniques (chaînes) avec leurs sources.

### 2.2. `classify.py`
Ce module est chargé de la classification des articles en domaines académiques spécifiques.

#### Fonctions

- **`clean_area(area: str) -> str`**
  - **Description** : Nettoie une chaîne de domaine spécifique en la convertissant en minuscules et en supprimant les parenthèses.
  - **Arguments** :
    - `area` (str) : La zone spécifique à nettoyer.
  - **Retourne** : La zone spécifique nettoyée.

- **`classify_article(article_text: str) -> List[str]`**
  - **Description** : Classifie un article dans des domaines académiques spécifiques et retourne une liste de domaines spécifiques.
  - **Arguments** :
    - `article_text` (str) : Le texte de l'article à classifier.
  - **Retourne** : Une liste de domaines spécifiques liés à l'article.

- **`classify_articles(articles: List[str]) -> List[str]`**
  - **Description** : Classifie plusieurs articles et retourne une liste de domaines liés à chaque article.
  - **Arguments** :
    - `articles` (list) : Une liste de textes d'articles à classifier.
  - **Retourne** : Une liste de domaines spécifiques liés aux articles.

### 2.3. `match.py`
Ce module propose des experts basés sur les mots-clés de leurs travaux, en utilisant des modèles d'intelligence artificielle.

#### Fonctions

- **`propose_experts_using_ai(thesis_title: str, num_experts: int = 3) -> list[dict]`**
  - **Description** : Utilise le modèle d'IA génératif pour proposer des experts en fonction des mots-clés (mot_clé) liés à un titre de thèse.
  - **Arguments** :
    - `thesis_title` (str) : Le titre de la thèse pour laquelle des experts sont proposés.
    - `num_experts` (int) : Le nombre d'experts à proposer (par défaut 3).
  - **Retourne** : Une liste de dictionnaires, chacun contenant 'name', 'keywords' et 'explanation' d'un expert.

## Utilisation
Pour utiliser l'application `data_classification`, vous pouvez appeler les fonctions définies dans chaque module selon les besoins de votre projet. Par exemple, pour récupérer des données de chercheur, utilisez `fetch_researcher_data`, et pour classifier des articles, utilisez `classify_article` ou `classify_articles`.
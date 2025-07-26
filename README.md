# Platform for Automated Recommendations of Experts for PhD Thesis Review

## Overview

This project aims to develop a platform that automatically recommends experts for PhD thesis evaluations by matching keywords between doctoral candidates' research interests and expert profiles. The platform seeks to streamline the reviewer selection process through the application of machine learning techniques.

## Features

- **Expert Database:** A comprehensive collection of experts categorized into:
  - **Algerian Experts:** Both internal and external to the university.
  - **International Experts:** Those with whom collaborations have been established.

- **Focus Areas:** Primarily focused on **Computer Science** and **Applied Mathematics**.

- **Recommendation System:** Utilizes machine learning methods to optimize expert recommendations, including:
  - **Decision Trees** for expert assignments.
  - **Clustering** techniques to group similar expert profiles.

- **Data Sources:** Enriches expert profiles using platforms like Google Scholar and ResearchGate.

## Installation

To get started with this project, clone the repository and follow the installation instructions:

```bash
git clone https://github.com/dynahym/Expert-Match.git
cd Expert-Match
```

### Dependencies

Install the required dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. **Setup Database:** Configure the expert database with the necessary data.
2. **Démarrer le serveur Django** :
   Exécutez la commande suivante :
   ```bash
   python manage.py runserver
   ```

## Documentation

For detailed documentation on the Django project, refer to [Documentation](backend/docs).

## Contact

For any inquiries or suggestions, please contact [ld_alismail@esi.dz](mailto:ld_alismail@esi.dz).

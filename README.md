# Platform for Automatic Expert Recommendations for PhD Thesis Review

## Overview

This project is designed to build a platform that automatically recommends experts for PhD thesis evaluations based on keyword matching between doctoral candidates' research interests and expert profiles. The platform aims to streamline the process of finding suitable reviewers by leveraging machine learning techniques.

## Features

- **Expert Database:** A comprehensive database of experts, categorized into:
  - **Algerian Experts:** Internal to the university and external.
  - **International Experts:** With whom collaborations have occurred.

- **Focus Areas:** Primarily in **Computer Science** and **Applied Mathematics**.

- **Recommendation System:** Incorporates machine learning techniques to enhance expert recommendations:
  - **Decision Trees** for expert assignment.
  - **Clustering** to group similar expert profiles.

- **Data Sources:** Enrichment of expert profiles using platforms like Google Scholar and ResearchGate.

## Installation

To get started with this project, clone the repository and follow the installation instructions:

```bash
git clone https://github.com/dynahym/expert_match_backend.git
cd expert_match_backend
```

### Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. **Setup Database:** Configure the expert database with the necessary data.
2. **Run the Recommendation System:** Execute the recommendation algorithm to generate expert suggestions based on research interests.

```bash
python main.py
```

## Contact

For any inquiries or suggestions, please contact [ld_alismail@esi.dz](mailto:ld_alismail@esi.dz).

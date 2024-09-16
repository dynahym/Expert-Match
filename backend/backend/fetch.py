from typing import List, Tuple
from data_collection.gate import get_gate_articles_interests, get_gate_profile_url
from data_collection.scholar import get_scholar_articles_interests
from data_collection.dblp import get_dblp_articles
from data_cleaning.clean import remove_duplicates
from data_cleaning.translate import translate_texts


def fetch_researcher_data(first_name: str, last_name: str) -> Tuple[List[str], List[str]]:
    """
    Retrieve researcher data (articles, interests) from ResearchGate, DBLP, and Google Scholar.

    Args:
        first_name (str): The researcher's first name.
        last_name (str): The researcher's last name.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists:
            - A list of article titles (strings).
            - A list of research interests (strings).
    """
    articles, interests = [], []

    # DBLP
    name = f"{first_name} {last_name}"
    dblp_articles = get_dblp_articles(name)
    articles.extend(remove_duplicates(translate_texts(dblp_articles))) if dblp_articles else None

    # Google Scholar
    gs_interests, gs_articles = get_scholar_articles_interests(name)
    articles.extend(remove_duplicates(translate_texts(gs_articles))) if gs_articles else None
    interests.extend(remove_duplicates(gs_interests)) if gs_interests else None
    
    # ResearchGate
    profile_url = get_gate_profile_url(first_name, last_name)
    if profile_url:
        rg_interests, rg_articles = get_gate_articles_interests(profile_url)
        articles.extend(remove_duplicates(translate_texts(rg_articles))) if rg_articles else None
        interests.extend(remove_duplicates(rg_interests)) if rg_interests else None

    unique_articles = remove_duplicates(articles)
    unique_interests = remove_duplicates(interests)

    return unique_articles, unique_interests

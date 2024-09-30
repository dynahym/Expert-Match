from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from data_collection.gate import get_gate_articles_interests
from data_collection.scholar import get_scholar_articles_interests
from data_collection.dblp import get_dblp_articles
from data_cleaning.clean import remove_duplicates
from data_cleaning.translate import translate_texts
from data_classification.classifier import classify_articles

def fetch_researcher_data(first_name: str, last_name: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Retrieve researcher data (articles, interests) from DBLP, Google Scholar, and ResearchGate in parallel.

    Args:
        first_name (str): The researcher's first name.
        last_name (str): The researcher's last name.

    Returns:
        Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]: A tuple containing two lists:
            - A list of unique article titles (strings) with their sources.
            - A list of unique research interests (strings) with their sources.
    """
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        dblp_future = executor.submit(get_dblp_articles, f"{first_name} {last_name}")
        gs_future = executor.submit(get_scholar_articles_interests, f"{first_name} {last_name}")
        rg_future = executor.submit(get_gate_articles_interests, first_name, last_name)

        # Retrieve results
        dblp_articles = dblp_future.result()
        gs_interests, gs_articles = gs_future.result()
        rg_interests, rg_articles = rg_future.result()

    # Combine all articles and translate them
    all_articles = dblp_articles + gs_articles + rg_articles
    translated_articles = translate_texts(all_articles)
    unique_articles = remove_duplicates(translated_articles)
    
    articles = []  # Initialize articles list
    for article in unique_articles:
        article_source = 'Autre'
        if article in gs_articles:
            article_source = 'Google Scholar'
        elif article in rg_articles:
            article_source = 'ResearchGate'
        elif article in dblp_articles:
            article_source = 'DBLP'
        
        if article_source:  # Append only if a source was found
            articles.append((article.capitalize(), article_source))
    
    # Classify interests and compile unique interests
    cls_interests = classify_articles(unique_articles)
    all_interests = gs_interests + rg_interests + cls_interests
    unique_interests = list(set(all_interests))
    unique_interests.sort()  # Sort interests alphabetically
    
    interests = []
    for interest in unique_interests:
        interest_source = 'Classified'
        if interest in gs_interests:
            interest_source = 'Google Scholar'
        elif interest in rg_interests:
            interest_source = 'ResearchGate'
        
        interests.append((interest.title(), interest_source))
    
    return articles, interests

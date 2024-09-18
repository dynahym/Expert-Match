from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Dict
from data_collection.gate import get_gate_articles_interests
from data_collection.scholar import get_scholar_articles_interests
from data_collection.dblp import get_dblp_articles
from data_cleaning.clean import remove_duplicates
from data_cleaning.translate import translate_texts

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
    dblp_articles, gs_articles, rg_articles = [], [], []
    gs_interests, rg_interests = [], []

    with ThreadPoolExecutor() as executor:
        # Submit tasks to fetch articles and interests from different sources
        dblp_future = executor.submit(get_dblp_articles, f"{first_name} {last_name}")
        gs_future = executor.submit(get_scholar_articles_interests, f"{first_name} {last_name}")
        rg_future = executor.submit(get_gate_articles_interests, first_name, last_name)

        # Collect results
        dblp_articles = dblp_future.result()
        gs_interests, gs_articles = gs_future.result()
        rg_interests, rg_articles = rg_future.result()

    # Combine articles with their sources
    all_articles = [(article, 'DBLP') for article in dblp_articles] \
                 + [(article, 'Google Scholar') for article in gs_articles] \
                 + [(article, 'ResearchGate') for article in rg_articles]
    all_interests = [(interest, 'Google Scholar') for interest in gs_interests] \
                 + [(interest, 'ResearchGate') for interest in rg_interests]

    # Extract titles and translate
    articles_titles = [article for article, _ in all_articles]
    translated_titles = translate_texts(articles_titles)
    
    # Create a mapping of translated titles to their original sources
    title_to_source = {}
    for (original_article, source), translated_article in zip(all_articles, translated_titles):
        title_to_source[translated_article] = source

    # Remove duplicates while preserving the source information
    unique_translated_titles = remove_duplicates(translated_titles)

    # Prepare the final list of unique articles with their sources
    unique_articles_with_sources = [(title, title_to_source[title]) for title in unique_translated_titles]

    return unique_articles_with_sources, list(set(all_interests))

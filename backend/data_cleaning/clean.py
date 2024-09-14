import re
from typing import List, Tuple
from fuzzywuzzy import fuzz
from data_collection.gate import get_gate_articles_interests, get_gate_profile_url
from data_collection.scholar import get_scholar_articles_interests
from data_collection.dblp import get_dblp_articles

def normalize_text(text: str) -> str:
    """
    Normalize text by converting to lowercase, removing special characters, and content between them.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    """
    text = re.sub(r'\$.*?\$|\[.*?\]', '', text.lower())  # Remove content between $ and [] and lower the case
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return re.sub(r'[^\w\s]', '', text).strip()  # Remove non-alphanumeric except spaces

def is_similar(text1: str, text2: str, threshold: int = 90) -> bool:
    """
    Check if two texts are similar based on a similarity threshold.

    Args:
        text1 (str): The first text.
        text2 (str): The second text.
        threshold (int, optional): The similarity threshold. Defaults to 90.

    Returns:
        bool: True if the texts are similar above the threshold, False otherwise.
    """
    return fuzz.ratio(text1, text2) > threshold

def remove_duplicates(data: List[str]) -> List[str]:
    """
    Remove duplicates from a list of articles based on a similarity threshold, keeping unique items.

    Args:
        data (List[str]): List of articles or strings to deduplicate.
        threshold (int, optional): The similarity threshold for detecting duplicates. Defaults to 90.

    Returns:
        List[str]: A list of unique articles after deduplication.
    """
    result = []
    seen_normalized = set()

    for item in data:
        normalized_item = normalize_text(item)
        if not any(is_similar(normalized_item, seen) for seen in seen_normalized):
            result.append(item)
            seen_normalized.add(normalized_item)

    return result


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
    
    # ResearchGate
    profile_url = get_gate_profile_url(first_name, last_name)
    if profile_url:
        rg_interests, rg_articles = get_gate_articles_interests(profile_url)
        articles.extend(remove_duplicates(rg_articles)) if rg_articles else None
        interests.extend(remove_duplicates(rg_interests)) if rg_interests else None

    # DBLP
    name = f"{first_name} {last_name}"
    articles.extend(remove_duplicates(get_dblp_articles(name)))

    # Google Scholar
    gs_interests, gs_articles = get_scholar_articles_interests(name)
    articles.extend(remove_duplicates(gs_articles)) if gs_articles else None
    interests.extend(remove_duplicates(gs_interests)) if gs_interests else None

    return articles, interests
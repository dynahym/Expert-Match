import sys
from typing import List, Tuple
from scholarly import scholarly

sys.stdout.reconfigure(encoding="utf-8")

def get_scholar_articles_interests(name: str) -> Tuple[List[str], List[str]]:
    """
    Searches for an author on Google Scholar and retrieves their research interests and publications.

    Args:
        name (str): The name of the author to search for.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists:
            - A list of research interests (strings) of the author.
            - A list of publication titles (strings) by the author.
    """
    search_query = scholarly.search_author(name)

    try:
        # Retrieve the first search result (the most relevant author)
        author = next(search_query)
    except StopIteration:
        print(f"SCHOLAR : No results found for author: {name}")
        return [], []

    # Retrieve detailed information about the author
    author_info = scholarly.fill(author)

    publications = [
        publication["bib"]["title"].lower()
        for publication in author_info["publications"]
    ]

    interests = author_info.get("interests", [])

    return interests, publications
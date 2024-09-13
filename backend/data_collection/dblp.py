import requests
from parsel import Selector
from .config import API_URL, HEADERS


def get_html_content(url):
    """
    Fetches HTML content from a given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the page, or an empty string if there was an error.
    """
    try:
        response = requests.get(url)  # Make a GET request to the URL
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text  # Return the HTML content
    except requests.RequestException as e:
        print(f"DBLP : Error fetching HTML content from {url}: {e}")
        return ""


def get_dblp_articles(author_name):
    """
    Searches for the most relevant author on DBLP and retrieves their publications.

    Args:
        author_name (str): The name of the author to search for.

    Returns:
        list: A list of article titles (in lowercase) or an empty list if no articles are found.
    """
    # Parameters for the API request
    params = {"q": author_name, "format": "json"}

    try:
        # Make a GET request to the DBLP API with the search parameters
        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"DBLP : Error fetching author data: {e}")
        return []

    data = response.json()
    # Extract the list of authors from the response
    authors = data.get("result", {}).get("hits", {}).get("hit", [])
    if not authors:
        print(f"DBLP : No results found for author: {author_name}")
        return []

    # Find the most relevent author
    best_author = max(authors, key=lambda a: float(a.get("score", 0)))
    author_info = best_author.get("info", {})
    author_url = author_info.get("url")
    if not author_url:
        print(f"DBLP : No URL found for author: {author_info.get('author', 'Unknown')}")
        return []

    # Fetch the HTML content of the author's DBLP page
    html_content = get_html_content(author_url)
    selector = Selector(text=html_content)
    articles = [
        article.css("::text").get().strip().lower()
        for article in selector.css(".title")
    ]

    if not articles:
        print("DBLP : No articles found or selector issue.")

    return articles
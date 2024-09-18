from typing import List, Tuple
from playwright.sync_api import sync_playwright
from parsel import Selector
import urllib.parse
from .config import USER_AGENT

def names_match(first_names: List[str], last_names: List[str], profile_names: List[str]) -> bool:
    """
    Checks if the profile names match the given first and last names.

    Args:
        first_names (List[str]): List of first names to match.
        last_names (List[str]): List of last names to match.
        profile_names (List[str]): List of names from the profile.

    Returns:
        bool: True if the profile names match the first and last names, otherwise False.
    """
    fn_matches = any(fn in profile_names for fn in first_names)
    ln_matches = all(ln in profile_names for ln in last_names)
    return fn_matches and ln_matches

def get_gate_articles_interests(first_name: str, last_name: str) -> Tuple[List[str], List[str]]:
    """
    Retrieves the research interests and publication titles from a ResearchGate profile
    based on the researcher's first and last names.

    Args:
        first_name (str): The first name of the researcher.
        last_name (str): The last name of the researcher.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists:
            - A list of research interests (strings).
            - A list of publication titles (strings).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch a headless browser
        page = browser.new_page(user_agent=USER_AGENT)  # Open a new page with a specified User-Agent

        try:
            # Prepare the query for ResearchGate search
            first_names = first_name.strip().lower().split()
            last_names = last_name.strip().lower().split()
            first_name_query = " OR ".join([f'"{name}"' for name in first_names])
            last_name_query = " OR ".join([f'"{name}"' for name in last_names])
            query = f"({first_name_query}) AND ({last_name_query})"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.researchgate.net/search/researcher?q={encoded_query}"
            page.goto(url, wait_until="domcontentloaded")  # Navigate to the search results page

            content = page.content()  # Get the page content
            selector = Selector(text=content)
            profiles = selector.css(".nova-legacy-v-entity-item__title")  # Select profile titles
            result = []

            for profile in profiles:
                profile_name = profile.css("a::text").get().replace("-", " ")
                profile_names = profile_name.strip().lower().split()
                if names_match(first_names, last_names, profile_names):
                    profile_url = profile.css("a").attrib["href"].split("?")[0]
                    profile_url = "https://www.researchgate.net/" + profile_url
                    result.append(profile_url)

            # Return the shortest URL from the results or an empty string if no results
            profile_url = min(result, key=len) if result else ""
            
            if not profile_url:
                return [], []
            
            page.goto(profile_url, wait_until="domcontentloaded")  # Navigate to the researcher's profile page
            selector = Selector(text=page.content())

            # Extract research interests
            interest_elements = selector.css(".js-target-skills > .nova-legacy-l-flex__item")
            interests = []
            if interest_elements:
                for interest in interest_elements:
                    interests.append(interest.css("::text").get())
            else:
                print("GATE : No interests found or selector issue.")

            # Extract publication titles
            article_elements = selector.css(".nova-legacy-v-publication-item__title")
            articles = []
            if article_elements:
                for article in article_elements:
                    articles.append(article.css("::text").get().lower())
            else:
                print("GATE : No articles found or selector issue.")

            return interests, articles

        except Exception as e:
            # Print any errors that occur during the process
            print(f"GATE : An error occurred: {e}")
            return [], []

        finally:
            browser.close()
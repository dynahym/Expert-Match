import google.generativeai as genai
import os, re
from dotenv import load_dotenv
from typing import List, Tuple

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API key must be set in the environment variable API_KEY.")

# Configure the Google Generative AI client with the API key
genai.configure(api_key=api_key)

def clean_area(area: str) -> str:
    """
    Cleans the specific area string by converting to lower case and removing parentheses.

    Args:
    - area (str): The specific area to clean.

    Returns:
    - str: The cleaned specific area.
    """
    # Use regex to remove text within parentheses and trim surrounding spaces
    cleaned_area = re.sub(r'\s*\(.*?\)\s*', ' ', area).strip()
    return cleaned_area.lower()


def classify_article(article_text: str) -> List[str]:
    """
    Classifies an article into specific academic domains and returns a list of specific areas.

    Args:
    - article_text (str): The text of the article to classify.

    Returns:
    - list: A list of specific areas related to the article.
    """
    # Create a prompt focused on specific areas
    prompt = (
        "You are an expert in classifying articles into academic domains. "
        "Classify the following article into academic domains and provide a **numbered list of specific areas only** without additional context: "
        f"{article_text}"
    )

    # Use the model to generate a classification response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Clean the response
    specific_areas_text = response.text.strip()

    # Use regex to extract the list items into a Python list
    specific_areas_list = re.findall(r'\d+\.\s+\*\*(.*?)\*\*', specific_areas_text)
    
    # Clean and extend the interests list with cleaned areas
    interests = []
    for area in specific_areas_list:
        area_list = area.split(', ')
        interests.extend(clean_area(area) for area in area_list)

    return interests

def classify_articles(articles: List[str]) -> List[str]:
    """
    Classifies multiple articles and returns a list of areas related to each article.

    Args:
    - articles (list): A list of article texts to classify.

    Returns:
    - list: A list of specific areas related to the article.
    """
    # Create a prompt focused on specific areas for all articles
    prompt = (
        "You are an expert in classifying articles into academic domains. "
        "Classify the following articles into academic domains and provide a **numbered list of specific areas only** without additional context:\n\n"
    )
    
    for index, article in enumerate(articles, start=1):
        prompt += f"{index}. {article}\n"

    # Use the model to generate a classification response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Clean the response
    specific_areas_text = response.text.strip().lower()
    # Use regex to extract the list items into a Python list
    specific_areas_list = re.findall(r'\d+\.\s+\*\*(.*?)\*\*', specific_areas_text)
    
    # Clean and extend the interests list with cleaned areas
    interests = []
    for area in specific_areas_list:
        area_list = area.split(', ')
        interests.extend(clean_area(area) for area in area_list)
    return interests

# Example usage
# article_text = (
#     "Various architectures and their applications in sentiment analysis."
# )

# # Classify a single article
# classified_areas = classify_article(article_text)
# print("Classified Areas for the Single Article:")
# for area in classified_areas:
#     print(f"- {area.title()}")

# # Example list of article texts
# articles = [
#     "Machine learning algorithms in biomedical applications.",
#     "The role of big data in modern healthcare.",
#     "Advancements in artificial intelligence for image recognition."
# ]

# # Classify multiple articles
# classified_areas_multiple = classify_articles(articles)
# print("\nClassified Areas for Multiple Articles:")
# for area in classified_areas_multiple:
#     print(f"- {area.title()}")

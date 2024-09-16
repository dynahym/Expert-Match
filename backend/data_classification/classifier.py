from transformers import pipeline, AutoTokenizer
from itertools import islice
from typing import List
from .config import CANDIDATE_LABELS, SUBCATEGORY_LABELS

model_name = 'facebook/bart-large-mnli'
tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
classifier = pipeline('zero-shot-classification', model=model_name, tokenizer=tokenizer)

def classify_article(article: str) -> List[str]:
    """
    Classify the article into broad and subcategories and return only the labels.

    Args:
        article (str): The text of the article to classify.

    Returns:
        List[str]: A list of subcategory labels, or [] if no subcategory is found.
    """
    broad_result = classifier(article, CANDIDATE_LABELS)
    broad_category = broad_result['labels'][broad_result['scores'].index(max(broad_result['scores']))]
    
    if broad_category in SUBCATEGORY_LABELS:
        subcategory_result = classifier(article, SUBCATEGORY_LABELS[broad_category])
        return subcategory_result['labels']
    
    return []


def classify_articles(articles: List[str], top_s: int = 10, top_t: int = 10) -> List[str]:
    """
    Process each article to classify it and return only the top subcategory labels.

    Args:
        articles (List[str]): A list of articles to process.
        top_s (int): The number of top subcategories to consider per article.
        top_t (int): The number of top labels to return based on total occurrences.

    Returns:
        List[str]: A list of the most frequent subcategory labels.
    """
    totals = {}

    for article in articles:
        subcategory_labels = classify_article(article)

        if subcategory_labels:
            for label in islice(subcategory_labels, top_s):
                totals[label] = totals.get(label, 0) + 1
    
    # Sort by frequency and return top_t labels only
    sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return [label for label, _ in sorted_totals[:top_t]]

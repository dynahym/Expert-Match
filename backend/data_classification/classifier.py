from transformers import pipeline, AutoTokenizer
from itertools import islice
from typing import List, Tuple, Dict
from .config import CANDIDATE_LABELS, SUBCATEGORY_LABELS

model_name = 'facebook/bart-large-mnli'
tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
classifier = pipeline('zero-shot-classification', model=model_name, tokenizer=tokenizer)

def classify_text(text: str) -> Tuple[str, List[str]]:
    """
    Classify the text into broad and subcategories and return the labels.

    Args:
        text (str): The text of the text to classify.

    Returns:
        Tuple[str, List[str]]: A tuple containing the broad category label and a list of subcategory labels.
    """
    broad_result = classifier(text, CANDIDATE_LABELS)
    broad_scores = broad_result['scores']
    broad_labels = broad_result['labels']
    
    # Identify the broad category with the highest score
    broad_category = broad_labels[broad_scores.index(max(broad_scores))]

    # If the broad category has associated subcategories, classify and return them
    subcategories = []
    if broad_category in SUBCATEGORY_LABELS:
        subcategory_result = classifier(text, SUBCATEGORY_LABELS[broad_category])
        subcategories = subcategory_result['labels']
    
    return broad_category, subcategories

def classify_texts(texts: List[str], top_s: int = 10, top_t: int = 10, batch_size: int = 8) -> List[str]:
    """
    Process each text to classify it and return only the top subcategory labels.

    Args:
        texts (List[str]): A list of texts to process.
        top_s (int): The number of top subcategories to consider per text.
        top_t (int): The number of top labels to return based on total occurrences.
        batch_size (int): The number of texts to classify in each batch.

    Returns:
        List[str]: A list of the most frequent subcategory labels.
    """
    totals: Dict[str, int] = {}

    # Process texts in batches
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        
        # Classify the batch of texts
        results = classifier(batch, CANDIDATE_LABELS)
        
        # Process each text's classification results
        for i, text in enumerate(batch):
            broad_result = results[i]
            broad_scores = broad_result['scores']
            broad_labels = broad_result['labels']
            
            broad_category = broad_labels[broad_scores.index(max(broad_scores))]

            subcategory_labels = []
            if broad_category in SUBCATEGORY_LABELS:
                subcategory_result = classifier(text, SUBCATEGORY_LABELS[broad_category])
                subcategory_labels = subcategory_result['labels']
            
            # Update counts for subcategory labels
            for label in islice(subcategory_labels, top_s):
                totals[label] = totals.get(label, 0) + 1
    
    # Sort by frequency and return top_t labels
    sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return [label for label, _ in sorted_totals[:top_t]]

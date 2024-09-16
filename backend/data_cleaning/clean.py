import warnings
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore", category=FutureWarning)

model = SentenceTransformer("all-MiniLM-L6-v2")

def encode_sentences(sentences: List[str]) -> List[np.ndarray]:
    """
    Encode a list of sentences into embeddings using the sentence-transformers model.

    Args:
        sentences (List[str]): List of sentences to encode.

    Returns:
        List[np.ndarray]: A list of sentence embeddings.
    """
    return model.encode(sentences)

def compute_similarity(embeddings: List[np.ndarray]) -> List[List[float]]:
    """
    Compute cosine similarity between embeddings.

    Args:
        embeddings (List[np.ndarray]): A list of sentence embeddings.

    Returns:
        List[List[float]]: A similarity matrix with cosine similarities between each pair of embeddings.
    """
    return cosine_similarity(embeddings)

def remove_duplicates(articles: List[str], threshold: float = 0.9) -> List[str]:
    """
    Remove duplicates from a list of articles based on a similarity threshold, keeping unique items.

    Args:
        articles (List[str]): List of articles or strings to deduplicate.
        threshold (float, optional): The similarity threshold for detecting duplicates. Defaults to 0.9.

    Returns:
        List[str]: A list of unique articles after deduplication.
    """
    if not articles:
        return []

    if len(articles) == 1:
        return articles

    embeddings = encode_sentences(articles)
    similarity_matrix = compute_similarity(embeddings)
    to_remove = set()

    for i in range(len(articles)):
        if i in to_remove:
            continue
        if len(articles[i].split()) < 3:
            to_remove.add(i)
            continue
        for j in range(i + 1, len(articles)):
            if similarity_matrix[i][j] >= threshold:
                to_remove.add(j)

    return [article for i, article in enumerate(articles) if i not in to_remove]

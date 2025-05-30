import numpy as np
from sentence_transformers import SentenceTransformer
import logging

# Global variable to store the model (lazy loading)
_model = None

def get_model():
    """
    Lazy loading of the SentenceTransformer model.
    This prevents issues during import and allows the app to start even if model loading fails.
    """
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            logging.info("SentenceTransformer model loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load SentenceTransformer model: {e}")
            raise e
    return _model

def compute_similarity(term, label):
    """
    Computes the semantic similarity between a term and a label using embeddings.

    Args:
        term (str): The term to compare.
        label (str): The label to compare.

    Returns:
        float: The cosine similarity between the embeddings of the term and the label.
    """
    try:
        model = get_model()
        term_embedding = model.encode(term)
        label_embedding = model.encode(label)
        
        # Cálculo da similaridade de cosseno entre os embeddings
        cosine_sim = np.dot(term_embedding, label_embedding) / (np.linalg.norm(term_embedding) * np.linalg.norm(label_embedding))
        return cosine_sim
    except Exception as e:
        logging.error(f"Error computing similarity: {e}")
        return 0.0

def filter_relevant_terms(similarity_dicts, threshold):
    """
    Filters terms based on their precomputed similarity scores.

    Args:
        similarity_dicts (list): A list of dictionaries in the format {"term": ..., "similarity": ...}.
        threshold (float): The similarity threshold for filtering terms.

    Returns:
        list: A list of terms (strings) that have a similarity score greater than or equal to the threshold.
    """
    if not similarity_dicts:  
        return []

    return [
        item["term"] for item in similarity_dicts
        if item.get("similarity", 0) >= threshold  
    ]


def is_prompt_related(label, key_terms, threshold):
    """
    Determines if an ontology label is relevant to the prompt based on semantic similarity.

    Args:
        label (str): The ontology label to evaluate.
        key_terms (list): A list of key terms extracted from the prompt.
        threshold (float): The similarity threshold for determining relevance.

    Returns:
        bool: True if the label is relevant to the prompt, False otherwise.
    """
    if not key_terms:
        print("Warning: No key terms provided to classify relevance.")
        return False

    highest_similarity = 0
    highest_label = None

    # Verificar a similaridade semântica entre o rótulo e os termos chave
    for key_term in key_terms:
        similarity = compute_similarity(label, key_term)
        if similarity > highest_similarity:
            highest_similarity = similarity
            highest_label = key_term

    # Se a similaridade for maior que o limiar, consideramos a relação relevante
    is_related = highest_similarity >= threshold and highest_label in key_terms

    return is_related
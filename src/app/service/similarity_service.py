import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(term, label):
    """
    Calcula a similaridade entre o termo e o rótulo usando embeddings semânticos.
    """
    term_embedding = model.encode(term)
    label_embedding = model.encode(label)
    
    # Cálculo da similaridade de cosseno entre os embeddings
    cosine_sim = np.dot(term_embedding, label_embedding) / (np.linalg.norm(term_embedding) * np.linalg.norm(label_embedding))
    return cosine_sim


def filter_relevant_terms(terms, original_prompt, threshold):
    """
    Filtra termos relevantes com base na similaridade semântica com o prompt original.
    Retorna uma lista de termos que são relevantes para o contexto geral do prompt.
    """
    relevant_terms = []
    for term in terms:
        similarity = compute_similarity(term, original_prompt)
        if similarity >= threshold:
            relevant_terms.append(term)
    return relevant_terms

def is_prompt_related(label, key_terms, threshold):
    """
    Verifica se o rótulo da ontologia é relevante para o prompt com base na similaridade semântica.
    Compara o rótulo com todos os termos-chave e retorna True se a similaridade for maior que o threshold.
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
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from owlready2 import get_ontology
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
import owlready2
import spacy

# Spacy
nlp = spacy.load("en_core_web_sm")

# Classificador de zero-shot
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Carregar o modelo pré-treinado do Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')

ontology_path = "public/ontology/MFOEM.owl"
onto = get_ontology(ontology_path).load()

def enrich_prompt(prompt: str):
    tokens = word_tokenize(prompt.lower())
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    freq_dist = FreqDist(filtered_tokens)
    key_terms = list(freq_dist.keys())

    matches_info = {}
    for term in key_terms:
        matches = search_ontology(term, key_terms)
        matches_info[term] = matches

    enriched_prompt = expand_prompt(prompt, matches_info, key_terms)

    return {
        "original_prompt": prompt,
        "enriched_prompt": enriched_prompt,
        "key_terms": key_terms,
        "ontology_matches": matches_info,
    }

def search_ontology(term, key_terms):
    results = []
    for entity in onto.classes():
        labels = entity.label or []  # Garantir que entity.label seja iterável
        for label in labels:
            # Verificar relação entre o termo e o rótulo
            if term.lower() in label.lower() and is_prompt_related(label, key_terms):
                entity_parents = get_entity_parents(entity)
                entity_children = get_entity_children(entity)
                results.append({
                    "identifier": entity.name,
                    "label": label,
                    "parents": entity_parents,
                    "children": entity_children,
                })
    return results

def get_entity_parents(entity):
    parents = []
    for parent in entity.is_a:
        if isinstance(parent, owlready2.ThingClass) and parent.label:
            parents.extend(parent.label)  # 'label' pode ser uma lista
    return parents

def get_entity_children(entity):
    children = []
    for child in entity.subclasses():
        if child.label:
            children.extend(child.label)
    return children

def is_prompt_related(label, key_terms, threshold=0.6):
    """
    Verifica se o rótulo da ontologia é relevante para o prompt com base na similaridade semântica.
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
    print(f"[DEBUG] Label: '{label}', Best Match: '{highest_label}', Similarity: {highest_similarity}, Related: {is_related}")

    return is_related

def compute_similarity(term, label):
    """
    Calcula a similaridade entre o termo e o rótulo usando embeddings semânticos.
    """
    term_embedding = model.encode(term)
    label_embedding = model.encode(label)
    
    # Cálculo da similaridade de cosseno entre os embeddings
    cosine_sim = np.dot(term_embedding, label_embedding) / (np.linalg.norm(term_embedding) * np.linalg.norm(label_embedding))
    return cosine_sim

def expand_prompt(original_prompt, ontology_matches, key_terms):
    enriched_prompt = original_prompt

    max_questions_per_term = 2
    total_questions_limit = 10  
    total_questions = 0

    for term in key_terms:
        if term in ontology_matches:
            matches = ontology_matches[term]
            if matches:
                for match in matches:
                    if total_questions >= total_questions_limit:
                        break 

                    parents = match.get("parents", [])
                    children = match.get("children", [])
                    term_label = match.get("label", "")

                    # Adicionar perguntas relacionadas a pais e filhos
                    if parents and total_questions < total_questions_limit:
                        enriched_prompt += f" What is the relationship between {', '.join(parents[:1])} and {term_label}?"
                        total_questions += 1
                    if children and total_questions < total_questions_limit:
                        enriched_prompt += f" What is the relationship between {', '.join(children[:1])} and {term_label}?"
                        total_questions += 1

                    if total_questions >= max_questions_per_term:
                        break

    # Adicionar contexto adicional baseado na classificação
    classification = classifier(original_prompt, key_terms)
    best_class = classification["labels"][0]
    filtered_key_terms = [term for term in key_terms if term != best_class]

    # Incorporar perguntas finais com mais contexto
    if total_questions < total_questions_limit:
        enriched_prompt += f" Explore the {best_class} aspects of this topic and their connection to {', '.join(filtered_key_terms[:3])}."

    return enriched_prompt
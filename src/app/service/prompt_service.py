from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from owlready2 import get_ontology

# Carregando a ontologia
ontology_path = "public/ontology/MFOEM.owl"
onto = get_ontology(ontology_path).load()

# Função principal de enriquecimento (chamada pelo controller)
def enrich_prompt(prompt: str):
    # Lógica de extração de termos-chave do prompt inicial
    tokens = word_tokenize(prompt.lower())
    
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    freq_dist = FreqDist(filtered_tokens)
    key_terms = list(freq_dist.keys())

    # Loop para buscar correspondências de key_terms na ontologia
    matches_info = {}
    for term in key_terms:
        matches = search_ontology(term)
        matches_info[term] = matches
        print(f"Termo: {term} - Correspondências: {matches}")

    enriched_prompt = f"{prompt} (termos-chave: {', '.join(key_terms)})"
    return {
        "original_prompt": prompt,
        "enriched_prompt": enriched_prompt,
        "key_terms": key_terms,
        "ontology_matches": matches_info
    }

# Função de busca na ontologia
def search_ontology(term):
    results = []
    
    # Loop para buscar correspondências de "term" na ontologia
    for entity in onto.classes():  
        if entity.label:  
            for label in entity.label:
                if term.lower() in label.lower():  
                    # Se encontrar correspondência, adiciona ao resultado
                    results.append({"identifier": entity.name, "label": label})
    return results
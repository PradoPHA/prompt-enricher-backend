import owlready2
from owlready2 import get_ontology
from app.service.similarity_service import compute_similarity, filter_relevant_terms, is_prompt_related

ontology_path = "public/ontology/MFOEM.owl"
onto = get_ontology(ontology_path).load()

def search_ontology(term, key_terms, threshold):
    results = []
    for entity in onto.classes():
        labels = entity.label or []  # Garantir que entity.label seja iterável
        for label in labels:
            # Verificar relação entre o termo e o rótulo
            if term.lower() in label.lower() and is_prompt_related(label, key_terms, threshold):
                entity_parents = get_entity_parents(entity)
                entity_children = get_entity_children(entity)
                entity_siblings = get_entity_siblings(entity)
                entity_ancestors = get_entity_ancestors(entity)

                results.append({
                    "identifier": entity.name,
                    "label": label,
                    "parents": entity_parents,
                    "children": entity_children,
                    "siblings": entity_siblings,
                    "ancestors": entity_ancestors,
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

def get_entity_siblings(entity):
    siblings = []
    for parent in entity.is_a:
        if isinstance(parent, owlready2.ThingClass):
            for child in parent.subclasses():
                if child != entity and child.label:
                    siblings.extend(child.label)
    return siblings

def get_entity_ancestors(entity):
    ancestors = []
    for parent in entity.is_a:
        if isinstance(parent, owlready2.ThingClass):
            ancestors.extend(parent.label or [])
            # Recursivamente buscar ancestrais
            ancestors.extend(get_entity_ancestors(parent))
    return list(set(ancestors))  # Remover duplicatas

def expand_prompt(original_prompt, ontology_matches, key_terms, threshold):
    # Iniciar com o prompt original
    enriched_prompt = original_prompt

    # Lista para armazenar frases adicionais
    additional_phrases = []

    max_questions_per_term = 3  # Número de perguntas por termo
    total_questions_limit = 15  # Limite total de perguntas
    total_questions = 0

    for term in key_terms:
        if term in ontology_matches:
            matches = ontology_matches[term]
            if matches:
                # Ordenar matches por relevância semântica em relação ao prompt
                matches = sorted(matches, key=lambda match: compute_similarity(term, match["label"]), reverse=True)
                questions_per_term = 0
                for match in matches:
                    if total_questions >= total_questions_limit or questions_per_term >= max_questions_per_term:
                        break

                    term_label = match.get("label", "")
                    parents = match.get("parents", [])
                    children = match.get("children", [])
                    siblings = match.get("siblings", [])
                    ancestors = match.get("ancestors", [])

                    # Filtrar relações por relevância semântica com um limiar mais alto
                    relevant_parents = filter_relevant_terms(parents, original_prompt, threshold)
                    relevant_children = filter_relevant_terms(children, original_prompt, threshold)
                    relevant_siblings = filter_relevant_terms(siblings, original_prompt, threshold)
                    relevant_ancestors = filter_relevant_terms(ancestors, original_prompt, threshold)

                    # Adicionar frases relacionadas a pais, filhos, irmãos e ancestrais
                    if relevant_parents and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        phrase = generate_dynamic_phrase(term_label, relevant_parents[:1], "influenced by")
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

                    if relevant_children and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        phrase = generate_dynamic_phrase(term_label, relevant_children[:1], "related to")
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

                    if relevant_siblings and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        phrase = generate_dynamic_phrase(term_label, relevant_siblings[:1], "related to")
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

                    if relevant_ancestors and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        phrase = generate_dynamic_phrase(term_label, relevant_ancestors[:1], "rooted in")
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

    enriched_prompt += " " + " ".join(additional_phrases)
    return enriched_prompt

def generate_dynamic_phrase(term, related_terms, relationship):
    """
    Gera uma frase dinâmica com base no termo, termos relacionados e o tipo de relação.
    """
    if relationship == "influenced by":
        return f"Considering that {term} is influenced by {', '.join(related_terms)}, how might this play a role in the process?"
    elif relationship == "affects":
        return f"Additionally, since {term} affects {', '.join(related_terms)}, what impact could this have?"
    elif relationship == "related to":
        return f"Interestingly, {term} is related to {', '.join(related_terms)}. How might this connection be significant?"
    elif relationship == "rooted in":
        return f"Fundamentally, {term} is rooted in {', '.join(related_terms)}. What broader implications does this suggest?"
    else:
        return f"The term {term} has a relationship with {', '.join(related_terms)}. How might this be important?"


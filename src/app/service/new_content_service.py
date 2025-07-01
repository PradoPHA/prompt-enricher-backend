import random
import string
from app.service.similarity_service import filter_relevant_terms

PHRASE_TEMPLATES = {
    "influenced by": [
        "{A} is influenced by {B}. How might this affect its role?",
        "What role does {B} play in shaping {A}?",
        "{A} may be shaped by {B}. Could this influence its relationship with other concepts?",
    ],
    "affects": [
        "{A} may affect {B}. What might be the consequences?",
        "Could {A}'s influence on {B} reveal deeper insights?",
        "How does {A} impact {B} in meaningful ways?",
    ],
    "related to": [
        "{A} seems closely related to {B}. Could this be significant?",
        "Exploring the link between {A} and {B}, what insights emerge?",
        "The relationship between {A} and {B} might offer new perspectives.",
    ],
    "rooted in": [
        "{A} appears to be rooted in {B}. What foundational role does this play?",
        "Is {A}'s origin tied to {B}? How might this matter?",
        "{B} might underlie {A}. What broader implications does this have?",
    ],
    "default": [
        "The term {A} has a relationship with {B}. How might this be important?",
        "What could the connection between {A} and {B} suggest?",
        "{A} and {B} share a link—what does this reveal?"
    ]
}

def has_ending_punctuation(text):
    """
    Checks if the given text ends with a punctuation mark.
    
    Args:
        text (str): The text to check.
        
    Returns:
        bool: True if the text ends with punctuation, False otherwise.
    """
    if not text or not text.strip():
        return False
    
    ending_punctuation = '.!?;:'
    return text.strip()[-1] in ending_punctuation

def expand_prompt(original_prompt, ontology_matches, key_terms, threshold):
    """
    Expands the original prompt by generating additional phrases based on ontology matches.

    Args:
        original_prompt (str): The original prompt provided by the user.
        ontology_matches (dict): A dictionary where keys are terms and values are lists of ontology matches.
        key_terms (list): A list of key terms extracted from the original prompt.
        threshold (float): The similarity threshold for filtering relevant terms.

    Returns:
        str: The enriched prompt with additional phrases based on ontology relationships.
    """
    if not has_ending_punctuation(original_prompt):
        enriched_prompt = original_prompt.rstrip() + "."
    else:
        enriched_prompt = original_prompt
    
    additional_phrases = []

    max_questions_per_term = 3
    total_questions_limit = 15
    total_questions = 0

    for term in key_terms:
        if term in ontology_matches:
            matches = ontology_matches[term]
            if matches:
                questions_per_term = 0
                for match in matches:
                    if total_questions >= total_questions_limit or questions_per_term >= max_questions_per_term:
                        break

                    term_label = match.get("label", "")
                    parents = match.get("parents", [])
                    children = match.get("children", [])
                    siblings = match.get("siblings", [])
                    ancestors = match.get("ancestors", [])         

                    relevant_parents = filter_relevant_terms(parents, threshold)
                    relevant_children = filter_relevant_terms(children, threshold)
                    relevant_siblings = filter_relevant_terms(siblings, threshold)
                    relevant_ancestors = filter_relevant_terms(ancestors, threshold)

                    if relevant_parents and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        relationship = pick_relationship_for_type("parents")
                        phrase = generate_dynamic_phrase(term_label, relevant_parents[:1], relationship)

                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

                    if relevant_children and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        relationship = pick_relationship_for_type("children")
                        phrase = generate_dynamic_phrase(term_label, relevant_children                                                                                           [:1], relationship)
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

                    if relevant_siblings and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        relationship = pick_relationship_for_type("siblings")
                        phrase = generate_dynamic_phrase(term_label, relevant_siblings[:1], relationship)
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

                    if relevant_ancestors and total_questions < total_questions_limit and questions_per_term < max_questions_per_term:
                        relationship = pick_relationship_for_type("ancestors")
                        phrase = generate_dynamic_phrase(term_label, relevant_ancestors[:1], relationship)
                        additional_phrases.append(phrase)
                        total_questions += 1
                        questions_per_term += 1

    if additional_phrases:
        # Montar um parágrafo coeso com conectores
        connectors = ["Additionally", "Moreover", "Interestingly", "Notably", "It is also worth noting that"]
        paragraph_sentences = []

        for i, phrase in enumerate(additional_phrases):
            if i == 0:
                paragraph_sentences.append(phrase)
            else:
                connector = connectors[i % len(connectors)]
                phrase_with_connector = f"{connector}, {phrase[0].lower() + phrase[1:]}"  # letra minúscula após vírgula
                paragraph_sentences.append(phrase_with_connector)

        # Opcional: encerrar com uma frase reflexiva
        closing_sentence = "Altogether, these relationships could enrich our understanding of the underlying concepts."

        enriched_prompt += "\n\n" + " ".join(paragraph_sentences) + " " + closing_sentence

    return enriched_prompt

def generate_dynamic_phrase(term_a, related_terms, relationship):
    """
    Generates a dynamic phrase based on the relationship between a term and related terms.

    Args:
        term_a (str): The main term for which the phrase is being generated.
        related_terms (list): A list of related terms to include in the phrase.
        relationship (str): The type of relationship (e.g., "influenced by", "affects").

    Returns:
        str: A dynamically generated phrase describing the relationship.
    """
    related = ', '.join(related_terms)
    templates = PHRASE_TEMPLATES.get(relationship, PHRASE_TEMPLATES["default"])
    template = random.choice(templates)
    return template.format(A=term_a, B=related)

def pick_relationship_for_type(relation_type):
    """
    Picks a relationship type based on the given relation type.

    Args:
        relation_type (str): The type of relation (e.g., "parents", "children", "siblings", "ancestors").

    Returns:
        str: A randomly selected relationship type corresponding to the given relation type.
    """
    mapping = {
        "parents": ["influenced by", "rooted in"],
        "children": ["affects", "related to"],
        "siblings": ["related to"],
        "ancestors": ["rooted in", "influenced by"],
    }
    return random.choice(mapping.get(relation_type, ["related to"]))

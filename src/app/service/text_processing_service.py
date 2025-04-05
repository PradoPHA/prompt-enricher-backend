import spacy

nlp = spacy.load("en_core_web_sm")

def extract_key_terms(prompt):
    """
    Extracts key terms from the given prompt by analyzing its linguistic structure.

    Args:
        prompt (str): The input prompt from which to extract key terms.

    Returns:
        list: A list of unique lemmatized key terms (strings) that are nouns, adjectives, or verbs.
    """
    doc = nlp(prompt.lower())
    # Aceita substantivos, adjetivos e verbos
    key_terms = list(set(token.lemma_ for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"]))
    return key_terms

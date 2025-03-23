import spacy

nlp = spacy.load("en_core_web_sm")

def extract_key_terms(prompt):
    doc = nlp(prompt.lower())
    # Aceita substantivos, adjetivos e verbos
    key_terms = list(set(token.lemma_ for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"]))
    return key_terms

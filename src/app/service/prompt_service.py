from sympy import false, true
from app.service.text_processing_service import extract_key_terms
from app.service.ontology_service import search_ontology
from app.service.new_content_service import expand_prompt
from pydantic import BaseModel

PRECISION_THRESHOLDS = {
    "very_low_precision": [0.2, 0.15, 0.1, 0.05],
    "low_precision": [0.4, 0.35, 0.3, 0.25],
    "medium_precision": [0.6, 0.55, 0.5, 0.45],
    "high_precision": [0.8, 0.75, 0.7, 0.65],
    "very_high_precision": [0.99, 0.95, 0.9, 0.85],
}

class PromptRequest(BaseModel):
    prompt: str
    precision: str

def enrich_prompt(promptRequest: PromptRequest):
    """
    Enriches a given prompt by analyzing its key terms, searching for related ontology matches, 
    and expanding the prompt with additional context based on the matches.

    Args:
        promptRequest (PromptRequest): An object containing the original prompt and the desired precision level.

    Returns:
        dict: A dictionary containing the enrichment status, the original and enriched prompts, 
              the threshold and precision level used, the extracted key terms, and the ontology matches.

    The function performs the following steps:
    1. Extracts key terms from the original prompt.
    2. Iterates through thresholds based on the specified precision level.
    3. Searches the ontology for matches related to the key terms.
    4. Expands the prompt with additional context based on the ontology matches.
    5. Returns the enriched prompt if it differs from the original; otherwise, returns a message indicating no enrichment.
    """
    key_terms = extract_key_terms(promptRequest.prompt)

    # Gets the list of thresholds corresponding to the given precision
    thresholds = PRECISION_THRESHOLDS.get(promptRequest.precision, [])

    for threshold in thresholds:
        matches_info = {term: search_ontology(term, key_terms, threshold, promptRequest.prompt) for term in key_terms}
        enriched_prompt = expand_prompt(promptRequest.prompt, matches_info, key_terms, threshold).strip()

        was_prompt_enriched = enriched_prompt != promptRequest.prompt

        if was_prompt_enriched:
            return {
                "Status": "Prompt enriched!",
                "Enriched": true,
                "Message": "The ontology matches were relevant enough for enrichment!",
                "Original Prompt": promptRequest.prompt,
                "Enriched Prompt": enriched_prompt,
                "Threshold used": threshold,
                "Precision level used": promptRequest.precision,
                "Key terms": key_terms,
                "Ontology matches": matches_info,
            }

    # If no threshold resulted in enrichment, return this response
    return {
        "Status": "Prompt not enriched!",
        "Enriched": false,
        "Message": "The ontology matches were not relevant enough for enrichment!",
        "Original Prompt": promptRequest.prompt,
        "Enriched Prompt": promptRequest.prompt,  # Returns the same, as there were no changes
        "Tried thesholds": thresholds,
        "Precision level used": promptRequest.precision,
        "Key terms": key_terms,
        "Ontology matches": matches_info,
    }

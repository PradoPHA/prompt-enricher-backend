from app.service.text_processing_service import extract_key_terms
from app.service.ontology_service import search_ontology
from app.service.ontology_service import expand_prompt
from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str
    threshold: float

def enrich_prompt(promptRequest: PromptRequest):
    key_terms = extract_key_terms(promptRequest.prompt)
    matches_info = {term: search_ontology(term, key_terms, promptRequest.threshold) for term in key_terms}
    enriched_prompt = expand_prompt(promptRequest.prompt, matches_info, key_terms, promptRequest.threshold).strip()

    was_prompt_enriched = enriched_prompt != promptRequest.prompt

    return {
        "Status": "Prompt enriquecido!" if was_prompt_enriched else "Prompt não enriquecido!",
        "Message": "As correspondências ontológicas foram relevantes o suficiente para o enriquecimento!" if was_prompt_enriched else "As correspondências ontológicas não foram relevantes o suficiente para o enriquecimento!",
        "Prompt original": promptRequest.prompt,
        "Prompt enriquecido": enriched_prompt,
        "Threshold utilizado": promptRequest.threshold,
        "Termos-chave": key_terms,
        "Correspondências na ontologia": matches_info,
    }
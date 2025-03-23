from app.service.text_processing_service import extract_key_terms
from app.service.ontology_service import search_ontology, expand_prompt
from pydantic import BaseModel

# Mapeamento de níveis de precisão para arrays de thresholds
PRECISION_THRESHOLDS = {
    "precisao_muito_baixa": [0.2, 0.15, 0.1, 0.05],
    "precisao_baixa": [0.4, 0.35, 0.3, 0.25],
    "precisao_media": [0.6, 0.55, 0.5, 0.45],
    "precisao_alta": [0.8, 0.75, 0.7, 0.65],
    "precisao_muito_alta": [0.99, 0.95, 0.9, 0.85],
}

class PromptRequest(BaseModel):
    prompt: str
    precision: str

def enrich_prompt(promptRequest: PromptRequest):
    key_terms = extract_key_terms(promptRequest.prompt)

    # Obtém a lista de thresholds correspondente à precisão informada
    thresholds = PRECISION_THRESHOLDS.get(promptRequest.precision, [])

    for threshold in thresholds:
        matches_info = {term: search_ontology(term, key_terms, threshold) for term in key_terms}
        enriched_prompt = expand_prompt(promptRequest.prompt, matches_info, key_terms, threshold).strip()

        was_prompt_enriched = enriched_prompt != promptRequest.prompt

        if was_prompt_enriched:
            return {
                "Status": "Prompt enriquecido!",
                "Message": "As correspondências ontológicas foram relevantes o suficiente para o enriquecimento!",
                "Prompt original": promptRequest.prompt,
                "Prompt enriquecido": enriched_prompt,
                "Threshold utilizado": threshold,
                "Nível de precisão utilizado": promptRequest.precision,
                "Termos-chave": key_terms,
                "Correspondências na ontologia": matches_info,
            }

    # Se nenhum threshold resultou em enriquecimento, retorna essa resposta
    return {
        "Status": "Prompt não enriquecido!",
        "Message": "As correspondências ontológicas não foram relevantes o suficiente para o enriquecimento!",
        "Prompt original": promptRequest.prompt,
        "Prompt enriquecido": promptRequest.prompt,  # Retorna igual, pois não houve mudanças
        "Threshold utilizado": None,  # Nenhum threshold funcionou
        "Nível de precisão utilizado": promptRequest.precision,
        "Termos-chave": key_terms,
        "Correspondências na ontologia": {},
    }

from fastapi import APIRouter
from pydantic import BaseModel
from app.service.prompt_service import enrich_prompt, PromptRequest
from app.service.similarity_service import compute_similarity

router = APIRouter()

class SimilarityRequest(BaseModel):
    prompt: str
    gpt_response: str

@router.post("/enrich_prompt")
def enrich_prompt_controller(request: PromptRequest):
    return enrich_prompt(request)

@router.post("/calculate_similarity")
def calculate_similarity_controller(request: SimilarityRequest):
    similarity_score = compute_similarity(request.prompt, request.gpt_response)
    
    return {
        "similarity": round(float(similarity_score), 2)
    }
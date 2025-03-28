from fastapi import APIRouter
from app.service.prompt_service import enrich_prompt, PromptRequest

router = APIRouter()

@router.post("/enrich_prompt")
def enrich_prompt_controller(request: PromptRequest):
    return enrich_prompt(request)
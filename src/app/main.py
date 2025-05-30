from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.prompt_controller import router as prompt_router
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Prompt Enricher Backend",
    description="Backend do sistema Prompt Enricher para enriquecimento de prompts utilizando processamento de linguagem natural e ontologias.",
    version="1.0.0"
)

# Configuração de CORS mais específica para produção
origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:8000",  # Local FastAPI
    "https://*.railway.app",  # Railway domains
    "https://*.vercel.app",   # Vercel domains (caso tenha frontend)
    "https://*.netlify.app",  # Netlify domains (caso tenha frontend)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desenvolvimento - em produção, use a lista 'origins' acima
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup_event():
    """
    Startup event to initialize models and services.
    """
    logger.info("Starting Prompt Enricher Backend...")
    try:
        # Pre-load models to catch any import errors early
        from app.service.similarity_service import get_model
        logger.info("Initializing SentenceTransformer model...")
        get_model()  # This will load the model
        logger.info("All models loaded successfully!")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # Don't raise the error - let the app start anyway
        logger.warning("App will continue without pre-loaded models")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event for cleanup.
    """
    logger.info("Shutting down Prompt Enricher Backend...")

@app.get("/")
def read_root():
    return {
        "message": "Prompt Enricher Backend está funcionando!",
        "status": "online",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Incluindo o router do controlador de prompts
app.include_router(prompt_router)

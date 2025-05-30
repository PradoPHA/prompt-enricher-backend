from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.prompt_controller import router as prompt_router
import os

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

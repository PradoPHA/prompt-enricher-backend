from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.prompt_controller import router as prompt_router

app = FastAPI()

# Adicionando o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/")
def read_root():
    return {"Aplicação iniciada em http://localhost:8000/!"}

# Incluindo o router do controlador de prompts
app.include_router(prompt_router)

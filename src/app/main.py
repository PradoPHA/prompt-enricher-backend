from fastapi import FastAPI
from app.controller.prompt_controller import router as prompt_router
import nltk

app = FastAPI()

@app.get("/")
def read_root():
    return {"Aplicação iniciada em http://localhost:8000/!"}

app.include_router(prompt_router)
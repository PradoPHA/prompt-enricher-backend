# Prompt Enricher Backend

Este é o back-end do sistema **Prompt Enricher**, desenvolvido com Python e FastAPI. Ele permite o enriquecimento de prompts utilizando processamento de linguagem natural e ontologias.

## **Como configurar o projeto**

1. **Ativar o ambiente virtual**  
   No terminal bash, execute:  
   source venv/Scripts/activate

2. **Instalar as dependências**  
   Instale as bibliotecas necessárias:  
   pip install -r requirements.txt

3. **Rodar o servidor**  
   Inicie o servidor localmente com o comando:  
    PYTHONPATH=src uvicorn src.app.main:app --host localhost --reload

   OBS.:

   - host localhost: Define que o servidor usará localhost como endereço.
   - reload: Habilita o modo de recarregamento automático para facilitar o desenvolvimento.

4. **Acessar o servidor**  
   O servidor estará disponível no endereço:
   - **API principal:** [http://localhost:8000/]

---

## **Observações**

- Certifique-se de utilizar o terminal **bash** para todos os comandos relativos ao desenvolvimento e o terminal **powershell** para todos os comantos relativos ao Git.
- Antes de subir novas alterações, adicione as dependências ao `requirements.txt` com o comando:
  pip freeze > requirements.txt

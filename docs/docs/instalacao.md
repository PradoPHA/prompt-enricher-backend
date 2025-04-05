# Guia de Instalação

Este documento descreve os passos necessários para configurar e executar o projeto **Prompt Enricher Backend** localmente.

---

## Requisitos

- Python 3.11.9
- `virtualenv` instalado
- Terminal Bash (para comandos de desenvolvimento)
- Terminal PowerShell (para comandos Git, conforme preferências do projeto)

---

## Passo a Passo

### 1. Criar e ativar o ambiente virtual

Caso ainda não exista um ambiente virtual criado:

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
source venv/Scripts/activate
```

---

### 2. Instalar dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

---

### 3. Executar o servidor localmente

Utilize o seguinte comando para iniciar o servidor FastAPI:

```bash
PYTHONPATH=src uvicorn src.app.main:app --host localhost --reload
```

**Observações sobre o comando acima:**

- `host localhost`: Define o endereço do servidor como `localhost`.
- `reload`: Habilita o recarregamento automático sempre que o código for alterado.

---

### 4. Acessar a aplicação

Após iniciar o servidor, acesse:

- API principal: [http://localhost:8000/](http://localhost:8000/)

---

## Dicas de Desenvolvimento

- Use o **terminal bash** para comandos relacionados ao ambiente Python e execução do servidor.
- Use o **PowerShell** para comandos Git.
- Sempre que adicionar bibliotecas novas, atualize o arquivo `requirements.txt` com:

```bash
pip freeze > requirements.txt
```
